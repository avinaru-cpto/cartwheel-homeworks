"""Read-only trace adapters and a synchronous Langfuse bridge.

Use the supplied single-record normalizer, never normalize_traces: the latter
merges scenario retries and loses the individual IDs needed for HW4 scores.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from analysis.helpers.normalization import _metadata, normalize_trace

ROOT = Path(__file__).resolve().parents[2]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def chronology(value: str | None) -> float:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).timestamp()
    except (ValueError, TypeError, AttributeError):
        return float("inf")


class SourceError(RuntimeError):
    pass


class LangfuseBridge:
    """Use the existing local credentials; never return them to the browser.

    HTTP errors are summarized without response bodies, which can contain
    credentials or raw trace content. A stable score id AND timestamp allow
    safe retries and corrections, including on a later calendar day.
    """

    def __init__(self):
        self.host = os.environ.get("LANGFUSE_HOST", "").rstrip("/")
        self.public = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        self.secret = os.environ.get("LANGFUSE_SECRET_KEY", "")
        self.configs: dict[str, str] = {}

    @property
    def configured(self) -> bool:
        return bool(self.host and self.public and self.secret)

    def request(self, path: str, body: Any = None) -> Any:
        if not self.configured:
            raise SourceError("Langfuse credentials are not configured in .env.")
        auth = base64.b64encode(f"{self.public}:{self.secret}".encode()).decode()
        req = urllib.request.Request(
            self.host + "/api/public/" + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": "Basic " + auth, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raise SourceError(f"Langfuse returned HTTP {exc.code}.") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise SourceError("Langfuse is unreachable or timed out. Check the local service.") from None

    def traces(self, scenario_ids: set[str] | None = None) -> list[dict]:
        summaries = []
        page = 1
        while True:
            result = self.request(f"traces?page={page}&limit=100")
            batch = result.get("data", [])
            summaries.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        # Summary metadata is sufficient for this project; records missing
        # metadata are fetched too so instrumentation differences lose no data.
        candidates = []
        for item in summaries:
            sid = _metadata(item).get("cartwheel.scenario_id")
            if not sid or scenario_ids is None or sid in scenario_ids:
                candidates.append(item)
        def fetch(item):
            return self.request("traces/" + urllib.parse.quote(item["id"], safe=""))
        with ThreadPoolExecutor(max_workers=4) as pool:
            full = list(pool.map(fetch, candidates))
        return [r for r in full if scenario_ids is None or scenario_id(r) in scenario_ids]

    @staticmethod
    def score_name(name: str) -> str:
        """Map a canonical mode to Langfuse's 35-character configuration name.

        Keep ordinary names unchanged. Long names retain a readable prefix and
        a stable digest; local mode names, label IDs and score IDs do not change.
        """
        if len(name) <= 35:
            return name
        return name[:22] + "_" + hashlib.sha256(name.encode()).hexdigest()[:12]

    def score_config(self, name: str) -> str:
        if name in self.configs:
            return self.configs[name]
        remote_name = self.score_name(name)
        page = 1
        while True:
            rows = self.request(f"score-configs?page={page}&limit=100").get("data", [])
            for row in rows:
                if row.get("name") == remote_name and not row.get("isArchived"):
                    lower, upper = row.get("minValue"), row.get("maxValue")
                    if row.get("dataType") != "NUMERIC" or (lower is not None and lower > 0) or (upper is not None and upper < 1):
                        raise SourceError("The existing score configuration does not accept numeric 0/1 judgments.")
                    self.configs[name] = row["id"]
                    return row["id"]
            if len(rows) < 100:
                break
            page += 1
        result = self.request("score-configs", {
            "name": remote_name, "dataType": "NUMERIC", "minValue": 0, "maxValue": 1,
            "description": "Human HW4 judgment: 1 = failure present, 0 = failure absent. Canonical mode: " + name,
        })
        self.configs[name] = result["id"]
        return result["id"]

    def write_score(self, label: dict) -> None:
        config_id = self.score_config(label["mode"])
        remote_name = self.score_name(label["mode"])
        label["langfuse_score_name"] = remote_name
        # The ingestion API explicitly accepts the stable event timestamp.
        # No SDK background queue: inspect every per-event error synchronously.
        result = self.request("ingestion", {"batch": [{
            "id": str(uuid.uuid4()), "type": "score-create", "timestamp": now(),
            "body": {
                "id": label["score_id"], "traceId": label["trace_id"],
                "name": remote_name, "value": label["label"],
                "dataType": "NUMERIC", "configId": config_id,
                "timestamp": label["score_timestamp"],
                "comment": label.get("evidence", "") + f" [human; mode {label['mode']}; revision {label['id']}]",
            },
        }]})
        if result.get("errors") or not result.get("successes"):
            raise SourceError("Langfuse did not acknowledge the score. The local judgment is queued for retry.")


def scenario_id(record: dict) -> str | None:
    found = record.get("cartwheel_scenario_id") or _metadata(record).get("cartwheel.scenario_id")
    if not found:
        for obs in record.get("observations", []):
            found = _metadata(obs).get("cartwheel.scenario_id")
            if found:
                break
    return str(found) if found else None


def adapt(record: dict, host: str = "") -> dict:
    trace = normalize_trace(record)
    metadata = trace["metadata"]
    session = metadata.get("cartwheel.session_id") or record.get("sessionId")
    if not session:
        session = next((_metadata(o).get("cartwheel.session_id") for o in record.get("observations", [])
                        if _metadata(o).get("cartwheel.session_id")), None)
    trace["session_id"] = str(session) if session else "trace:" + trace["trace_id"]
    trace["missing_session"] = not bool(session)
    trace["meta"].setdefault("scenario_id", scenario_id(record))
    trace["meta"].update({k: v for k, v in record.get("meta", {}).items() if k not in trace["meta"]})
    # The HW3 exporter carries merchant authorization scope on tool spans,
    # even when the root trace has no store attribute. Do not infer scope from
    # an order's store_id: an authorized support lookup can concern any store.
    if "store" not in trace["meta"]:
        scopes = {str(_metadata(o)["cartwheel.store_id"]) for o in record.get("observations", [])
                  if _metadata(o).get("cartwheel.store_id") is not None}
        if len(scopes) == 1:
            trace["meta"]["store"] = scopes.pop()
    if host and record.get("htmlPath", "").startswith("/project/"):
        trace["permalink"] = host + record["htmlPath"]
    # The supplied normalizer omits system messages and error span fields.
    # Keep them accessible without reprinting each generation's full history.
    systems, diagnostics = [], []
    for obs in sorted(record.get("observations", []), key=lambda o: chronology(o.get("startTime") or o.get("start_time"))):
        inp = obs.get("input")
        if isinstance(inp, dict):
            for message in inp.get("messages", []):
                if message.get("role") in {"system", "developer"} and message not in systems:
                    systems.append(message)
        if obs.get("level") in {"ERROR", "WARNING"} or obs.get("statusMessage"):
            diagnostics.append({k: obs.get(k) for k in ("id", "name", "level", "statusMessage", "startTime")})
    trace["system_messages"] = systems
    trace["diagnostics"] = diagnostics
    trace["has_reply"] = any(m.get("role") == "assistant" for m in trace["trace"])
    return trace


class TraceStore:
    def __init__(self, records: list[dict], source: dict, host: str = ""):
        self.source = source
        self.raw, self.traces = {}, {}
        self.sessions: dict[str, list[dict]] = defaultdict(list)
        for raw in records:
            trace = adapt(raw, host)
            tid = trace["trace_id"]
            if tid in self.traces:
                if self.raw[tid] != raw:
                    raise ValueError(f"Conflicting copies of trace {tid}; resolve the source before review.")
                continue
            self.raw[tid], self.traces[tid] = raw, trace
            self.sessions[trace["session_id"]].append(trace)
        for group in self.sessions.values():
            group.sort(key=lambda t: (chronology(t["timestamp"]), t["trace_id"]))

    def summaries(self) -> list[dict]:
        summaries = []
        for t in sorted(self.traces.values(), key=lambda t: (chronology(t["timestamp"]), t["trace_id"])):
            summaries.append({
                **{k: t[k] for k in ("trace_id", "session_id", "timestamp", "meta", "features", "has_reply", "missing_session")},
                "turns_in_session": len(self.sessions[t["session_id"]]),
                "prompt": next((m.get("text", "") for m in t["trace"] if m.get("role") == "user"), "No user message")[:260],
                "diagnostic_count": len(t["diagnostics"]),
            })
        return summaries


def load_store(source: str, bridge: LangfuseBridge, offline_reason: str = "") -> TraceStore:
    if source == "langfuse":
        path = ROOT / "scenarios/support_scenarios.jsonl"
        ids = {json.loads(line)["id"] for line in path.read_text().splitlines() if line.strip()} if path.exists() else None
        rows = bridge.traces(ids)
        if not rows:
            raise SourceError("No final HW3 scenario traces were found in the configured project.")
        info = {"kind": "langfuse", "description": "Live Langfuse · final HW3 scenarios", "loaded_at": now()}
    else:
        if not offline_reason.strip():
            raise ValueError("An offline source requires --offline-reason explaining why live Langfuse is unavailable.")
        path = Path(source).resolve()
        raw = json.loads(path.read_text())
        rows = raw.get("traces", []) if isinstance(raw, dict) else raw
        info = {"kind": "offline", "description": path.name, "reason": offline_reason, "loaded_at": now()}
    return TraceStore(rows, info, bridge.host)
