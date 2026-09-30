"""Validated, conflict-aware human review state, compatible with course files."""
from __future__ import annotations

import hashlib
import json
import random
import re
import threading
import uuid
from collections import Counter, defaultdict
from pathlib import Path

from analysis.helpers import _state
from analysis.helpers.selection import _feature_vector, _kmeans, _standardize
from .data import LangfuseBridge, TraceStore, now

BATCHES = {"uniform_initial": 15, "cluster": 15, "dimension": 30, "depth": 25, "uniform_final": 15}


class Conflict(ValueError):
    pass


def as_list(value, key):
    return value if isinstance(value, list) else value.get(key, []) if isinstance(value, dict) else []


def modes(value):
    if isinstance(value, dict) and "modes" in value:
        return value["modes"]
    return [{"name": name, **item} for name, item in value.items() if isinstance(item, dict)] if isinstance(value, dict) else []


def mode_revision(mode):
    fields = {key: mode.get(key) for key in ("definition", "boundary", "requirement_source", "example_trace_ids", "close_negative_trace_ids")}
    return hashlib.sha256(json.dumps(fields, sort_keys=True).encode()).hexdigest()[:16]


class ReviewState:
    def __init__(self, root: Path, traces: TraceStore, bridge: LangfuseBridge | None = None):
        self.root, self.traces, self.bridge = root, traces, bridge
        self.lock = threading.RLock()

    def read(self, name, default):
        return _state.read_json(self.root / name, default)

    def write(self, name, value):
        _state.write_json(self.root / name, value)

    def annotations(self):
        return as_list(self.read("annotations.json", []), "annotations")

    def active_annotations(self):
        return [a for a in self.annotations() if not a.get("deleted_at") and a.get("trace_id") in self.traces.traces]

    def reviewed(self):
        return {a["trace_id"] for a in self.active_annotations() if a.get("kind") in {"first_failure", "no_failure"}}

    def all_modes(self):
        return modes(self.read("patterns.json", {}))

    def label_rows(self, mode):
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", mode):
            raise ValueError("Mode names must use snake_case.")
        return _state.read_jsonl(self.root / "labels" / (mode + ".jsonl"))

    def labels(self):
        current = {}
        for mode in self.all_modes():
            for row in self.label_rows(mode["name"]):
                if row.get("trace_id") in self.traces.traces and not row.get("superseded_by"):
                    current[(mode["name"], row["trace_id"])] = row
        return list(current.values())

    def manifest(self):
        return self.read("sample_manifest.json", {"version": 1, "batches": [], "samples": []})

    def revision(self):
        digest = hashlib.sha256()
        paths = [self.root / n for n in ("annotations.json", "patterns.json", "suggestions.json", "sample_manifest.json")]
        paths += sorted((self.root / "labels").glob("*.jsonl")) if (self.root / "labels").exists() else []
        for path in paths:
            digest.update(path.name.encode())
            digest.update(path.read_bytes() if path.exists() else b"missing")
        return digest.hexdigest()

    def snapshot(self):
        with self.lock:
            patterns = self.all_modes()
            labels = self.labels()
            final = {m["name"]: m for m in patterns if m.get("status") == "final"}
            reviewed = self.reviewed()
            manifest = self.manifest()
            sample_ids = {s["trace_id"] for s in manifest.get("samples", [])}
            counted = reviewed & sample_ids
            valid = [row for row in labels if row["trace_id"] in counted and row["mode"] in final
                     and row.get("mode_revision") == mode_revision(final[row["mode"]])]
            return {
                "revision": self.revision(), "source": self.traces.source,
                "traces": self.traces.summaries(), "annotations": self.active_annotations(),
                "patterns": patterns, "suggestions": as_list(self.read("suggestions.json", []), "suggestions"),
                "manifest": manifest, "labels": labels,
                "progress": {"reviewed": len(counted), "inspected": len(reviewed), "sampled": len(sample_ids),
                             "target": 100, "final_modes": len(final), "decisions": len(valid),
                             "missing": len(counted) * len(final) - len(valid),
                             "pending_sync": sum(r.get("sync_status") != "synced" for r in labels),
                             "batches": [{"name": name, "target": target,
                                          "selected": sum(s.get("batch") == name for s in manifest.get("samples", [])),
                                          "reviewed": sum(s.get("batch") == name and s["trace_id"] in reviewed for s in manifest.get("samples", []))}
                                         for name, target in BATCHES.items()]},
            }

    def mutate(self, action, body):
        with self.lock:
            if body.get("revision") != self.revision():
                raise Conflict("Review state changed in another tab or process. Refresh and reapply your saved draft.")
            operations = {"annotation": self.annotation, "label": self.label,
                          "suggestion": self.suggestion, "mode": self.mode,
                          "batch": self.batch, "sync": self.sync}
            if action not in operations:
                raise ValueError("Unknown operation.")
            result = operations[action](body)
            return {"ok": True, "result": result, "revision": self.revision()}

    def require_trace(self, tid):
        if tid not in self.traces.traces:
            raise ValueError("The trace ID is not in the loaded source.")

    def validate_anchor(self, tid, idx, quote):
        self.require_trace(tid)
        if idx is not None:
            messages = self.traces.traces[tid]["trace"]
            if type(idx) is not int or not 0 <= idx < len(messages):
                raise ValueError("The selected message no longer exists.")
            message = messages[idx]
            value = message.get("arguments") if message.get("role") == "tool_call" else message.get("text", message.get("content", ""))
            text = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
            if quote and quote not in text:
                raise ValueError("The quote does not match the selected evidence.")

    def annotation(self, body, source="human"):
        tid = body.get("trace_id")
        self.require_trace(tid)
        note = str(body.get("note", "")).strip()
        kind = body.get("kind", "first_failure")
        if kind not in {"first_failure", "no_failure", "observation"}:
            raise ValueError("Initial review records free-text observations, not failure modes.")
        if body.get("mode") or "label" in body:
            raise ValueError("Open coding must not assign a mode or binary label.")
        if kind == "no_failure":
            note = "no failure observed"
        if not note or len(note) > 20000:
            raise ValueError("Write a note of 1–20,000 characters.")
        raw = self.read("annotations.json", [])
        rows = as_list(raw, "annotations")
        aid = body.get("id") or str(uuid.uuid4())
        previous = next((r for r in rows if r.get("id") == aid), None)
        if previous and previous["trace_id"] != tid:
            raise ValueError("An annotation cannot move to another trace.")
        if kind in {"first_failure", "no_failure"} and not body.get("delete"):
            existing = [a for a in rows if a.get("trace_id") == tid and a.get("kind") in {"first_failure", "no_failure"}
                        and not a.get("deleted_at") and a.get("id") != aid]
            if existing:
                raise ValueError("This trace already has an initial review. Edit that observation instead.")
        idx = body.get("idx")
        quote = str(body.get("quote", ""))
        self.validate_anchor(tid, idx, quote)
        record = {"id": aid, "trace_id": tid, "session_id": self.traces.traces[tid]["session_id"],
                  "kind": kind, "note": note, "quote": quote, "idx": idx,
                  "start": body.get("start"), "end": body.get("end"), "source": source, "ts": now()}
        if previous:
            record["history"] = previous.get("history", []) + [{k: v for k, v in previous.items() if k != "history"}]
            if body.get("delete"):
                record["deleted_at"] = now()
            rows[rows.index(previous)] = record
        else:
            if body.get("delete"):
                raise ValueError("Annotation not found.")
            rows.append(record)
        if isinstance(raw, dict):
            raw["annotations"] = rows
        else:
            raw = rows
        self.write("annotations.json", raw)
        return record

    def _save_label(self, body, source="human"):
        tid, name, value = body.get("trace_id"), body.get("mode"), body.get("label")
        self.require_trace(tid)
        mode = next((m for m in self.all_modes() if m["name"] == name), None)
        if not mode or mode.get("status") != "final":
            raise ValueError("Binary judgments require a human-finalized mode.")
        if tid not in self.reviewed():
            raise ValueError("Complete the initial open-coding review before structured labeling.")
        if type(value) is not int or value not in (0, 1):
            raise ValueError("Choose present (1) or absent (0). Missing is never absent.")
        evidence = str(body.get("evidence", "")).strip()
        if not evidence:
            raise ValueError("Add evidence explaining this judgment.")
        rows = self.label_rows(name)
        old = next((r for r in reversed(rows) if r.get("trace_id") == tid and not r.get("superseded_by")), None)
        if old and old["label"] == value and old.get("evidence") == evidence and old.get("mode_revision") == mode_revision(mode):
            return old
        timestamp = now()
        record = {"id": str(uuid.uuid4()), "trace_id": tid, "mode": name, "label": value,
                  "source": source, "evidence": evidence, "ts": timestamp,
                  "mode_revision": mode_revision(mode), "supersedes": old.get("id") if old else None,
                  "score_id": (old or {}).get("score_id") or str(uuid.uuid5(uuid.NAMESPACE_URL, "cartwheel-hw4:" + tid + ":" + name)),
                  "score_timestamp": (old or {}).get("score_timestamp") or timestamp,
                  "sync_status": "pending"}
        rows.append(record)
        path = self.root / "labels" / (name + ".jsonl")
        _state.write_jsonl(path, rows)
        # Persist first, then attempt the canonical write. A crash or outage
        # leaves a recoverable pending record rather than a lost human decision.
        self._sync_record(record)
        _state.write_jsonl(path, rows)
        return record

    def _sync_record(self, row):
        if not self.bridge or not self.bridge.configured or self.traces.source["kind"] != "langfuse":
            row["sync_status"] = "pending"
            row["sync_error"] = "Local only. Reopen with live Langfuse and retry synchronization."
            return
        try:
            self.bridge.write_score(row)
            row["sync_status"] = "synced"
            row["synced_at"] = now()
            row.pop("sync_error", None)
        except Exception:
            row["sync_status"] = "pending"
            row["sync_error"] = "Langfuse did not acknowledge this judgment. Retry from Progress."

    def label(self, body):
        return self._save_label(body)

    def sync(self, body):
        count = 0
        for mode in self.all_modes():
            if mode.get("status") != "final":
                continue
            rows = self.label_rows(mode["name"])
            latest = {r["trace_id"]: r for r in rows if not r.get("superseded_by")}
            for tid, row in latest.items():
                if tid in self.traces.traces and row.get("sync_status") != "synced" and row.get("mode_revision") == mode_revision(mode):
                    self._sync_record(row)
                    count += row.get("sync_status") == "synced"
            if rows:
                _state.write_jsonl(self.root / "labels" / (mode["name"] + ".jsonl"), rows)
        return {"synced": count}

    def suggestion(self, body):
        raw = self.read("suggestions.json", [])
        rows = as_list(raw, "suggestions")
        item = next((s for s in rows if s.get("id") == body.get("id")), None)
        if not item:
            raise ValueError("Suggestion not found.")
        if item.get("status", "pending") != "pending":
            raise ValueError("This suggestion has already been decided.")
        decision, reason = body.get("decision"), str(body.get("reason", "")).strip()
        if decision not in {"accepted", "rejected"} or not reason:
            raise ValueError("Accept or reject explicitly and record your reason.")
        if decision == "accepted":
            self.validate_anchor(item["trace_id"], item.get("idx"), item.get("quote", ""))
            if item["trace_id"] not in self.reviewed():
                raise ValueError("Complete the initial open-coding review before accepting a mode suggestion.")
            mode = next((m for m in self.all_modes() if m["name"] == item.get("mode")), None)
            if not mode or mode.get("status") == "retired":
                raise ValueError("The suggestion must refer to an existing candidate or final mode.")
            if mode.get("status") == "final":
                label = self._save_label({"trace_id": item["trace_id"], "mode": item.get("mode"),
                                          "label": item.get("label", 1), "evidence": reason}, "accepted_suggestion")
                item["label_id"] = label["id"]
            else:
                item["needs_final_label"] = True
            # Acceptance is a separate structured observation, never the
            # initial open code. Preserve the originating suggestion verbatim.
            self.annotation({"id": "accepted-" + str(item["id"]), "trace_id": item["trace_id"],
                             "kind": "observation", "note": reason, "quote": item.get("quote", ""), "idx": item.get("idx")}, "accepted_suggestion")
        item.update({"status": decision, "decision_reason": reason, "decided_at": now(), "decided_by": "human"})
        self.write("suggestions.json", raw)
        return item

    def mode(self, body):
        item = body.get("mode", {})
        name = item.get("name", "")
        self.label_rows(name)  # validate safe file name
        if not item.get("definition", "").strip():
            raise ValueError("Give the mode a binary definition.")
        if item.get("status") not in {"candidate", "final", "retired"}:
            raise ValueError("Choose candidate, final, or retired.")
        annotations = {a["id"]: a for a in self.active_annotations() if a.get("id")}
        origins = item.get("created_from", [])
        if not origins or any(a not in annotations for a in origins):
            raise ValueError("Every mode needs valid originating human annotation IDs.")
        for key in ("example_trace_ids", "close_negative_trace_ids"):
            if not isinstance(item.get(key, []), list):
                raise ValueError("Example IDs must be lists.")
            for tid in item.get(key, []):
                self.require_trace(tid)
        if set(item.get("example_trace_ids", [])) & set(item.get("close_negative_trace_ids", [])):
            raise ValueError("A trace cannot be both a positive example and a close negative for one mode.")
        if item["status"] == "final":
            positives = set(item.get("example_trace_ids", []))
            negatives = set(item.get("close_negative_trace_ids", []))
            if len(positives) < 3 or not positives <= self.reviewed():
                raise ValueError("A final mode needs at least three reviewed, human-confirmed positive traces.")
            if (len(negatives) < 3 and not item.get("close_negative_exception", "").strip()) or not negatives <= self.reviewed():
                raise ValueError("Provide three reviewed close negatives, or document why fewer are available.")
            if not item.get("boundary", "").strip() or not item.get("requirement_source", "").strip():
                raise ValueError("Document the neighboring-mode boundary and SPEC requirement or revision.")
            if item.get("evaluator_type") not in {"code", "llm_judge"}:
                raise ValueError("Choose a code check or an LLM judge.")
            if not body.get("human_confirmed"):
                raise ValueError("Finalization requires explicit human confirmation of the examples and boundary.")
        raw = self.read("patterns.json", {"modes": []})
        existing = modes(raw)
        old = next((m for m in existing if m["name"] == name), None)
        reason = str(body.get("reason", "")).strip()
        if old and not reason:
            raise ValueError("Record why this taxonomy definition changed.")
        item = {**item, "updated_at": now(), "updated_by": "human"}
        item["revision"] = mode_revision(item)
        if old:
            existing[existing.index(old)] = item
        else:
            existing.append(item)
        if "modes" not in raw:
            raw = {"modes": existing, "legacy_snapshot": raw}
        raw["modes"] = existing
        raw.setdefault("revisions", []).append({"ts": now(), "name": name, "reason": reason or "Initial human definition", "before": old, "after": item})
        self.write("patterns.json", raw)
        return item

    def batch(self, body):
        name = body.get("batch")
        if name not in BATCHES:
            raise ValueError("Choose a prescribed HW4 batch.")
        manifest = self.manifest()
        samples = manifest.setdefault("samples", [])
        if any(s.get("batch") == name for s in samples):
            raise ValueError("This batch is already recorded; sampling cannot replace earlier selections.")
        if name != "uniform_initial":
            prerequisites = {"cluster": ["uniform_initial"], "dimension": ["uniform_initial", "cluster"],
                             "depth": ["uniform_initial", "cluster", "dimension"],
                             "uniform_final": ["uniform_initial", "cluster", "dimension", "depth"]}[name]
            for previous in prerequisites:
                chosen = {s["trace_id"] for s in samples if s.get("batch") == previous}
                if len(chosen) < BATCHES[previous] or not chosen <= self.reviewed():
                    raise ValueError(f"Finish the {previous.replace('_', ' ')} batch before selecting this one.")
        used = {s["trace_id"] for s in samples} | self.reviewed()
        pool = sorted((t for tid, t in self.traces.traces.items() if tid not in used), key=lambda t: t["trace_id"])
        k, seed = BATCHES[name], body.get("seed", 20260918)
        if type(seed) is not int:
            raise ValueError("The sampling seed must be an integer.")
        if len(pool) < k:
            raise ValueError("Not enough distinct, unreviewed traces remain.")
        rng = random.Random(seed)
        reason = {"method": name, "seed": seed, "selected_at": now(), "source": self.traces.source}
        if name in {"uniform_initial", "uniform_final"}:
            if name == "uniform_final":
                # HW4 Part B calls for this batch after *drafting* the taxonomy.
                # It tests discovery/saturation; final-mode evidence checks still
                # belong to mode(), not to this uniform sampling prerequisite.
                taxonomy = [m for m in self.all_modes() if m.get("status") in {"candidate", "final"}]
                if not taxonomy:
                    raise ValueError("Draft a taxonomy before drawing the final uniform batch.")
                reason["taxonomy_at_selection"] = [
                    {"name": m["name"], "status": m["status"],
                     "definition": m["definition"], "revision": mode_revision(m)}
                    for m in taxonomy
                ]
            chosen = rng.sample(pool, k)
        elif name == "cluster":
            vectors = _standardize([_feature_vector(t) for t in pool])
            assignment = _kmeans(vectors, k=5, seed=seed)
            groups = defaultdict(list)
            for i, cluster in enumerate(assignment):
                groups[cluster].append(i)
            for cluster, indices in groups.items():
                center = [sum(vectors[i][d] for i in indices) / len(indices) for d in range(len(vectors[0]))]
                groups[cluster] = sorted(indices, key=lambda i: (sum((a-b)**2 for a,b in zip(vectors[i], center)), pool[i]["trace_id"]))
            chosen = []
            while len(chosen) < k:
                for group in groups.values():
                    if group and len(chosen) < k:
                        chosen.append(pool[group.pop(0)])
            reason["features"] = ["turn_count", "tool_call_count", "distinct_tools", "has_retrieval", "tokens"]
            reason["description"] = "Round-robin nearest-centroid representatives from five structural clusters."
        elif name == "dimension":
            dimension = body.get("dimension")
            if dimension not in {"role", "store", "prompt_version"}:
                raise ValueError("Choose the product dimension before drawing or inspecting this batch.")
            groups = defaultdict(list)
            for trace in pool:
                groups[str(trace["meta"].get(dimension, "unknown"))].append(trace)
            for group in groups.values():
                rng.shuffle(group)
            chosen = []
            while len(chosen) < k:
                for key in sorted(groups):
                    if groups[key] and len(chosen) < k:
                        chosen.append(groups[key].pop())
            reason.update({"dimension": dimension, "dimension_selected_at": now(), "allocation": dict(Counter(str(t["meta"].get(dimension, "unknown")) for t in chosen))})
        else:
            ids = body.get("trace_ids", [])
            if len(ids) != k or len(set(ids)) != k or not set(ids) <= {t["trace_id"] for t in pool}:
                raise ValueError("Depth search needs 25 distinct, previously unreviewed trace IDs outside earlier batches.")
            if not str(body.get("reason", "")).strip():
                raise ValueError("Record the search method and candidate modes for this depth batch.")
            chosen = [self.traces.traces[tid] for tid in ids]
            reason["search_reason"] = body["reason"]
        for t in chosen:
            samples.append({"trace_id": t["trace_id"], "session_id": t["session_id"], "batch": name})
        manifest.setdefault("batches", []).append({"name": name, "count": len(chosen), **reason})
        self.write("sample_manifest.json", manifest)
        return {"count": len(chosen), "batch": name}

    def graph(self):
        """Deterministic PCA of structural features; not a quality prediction."""
        traces = sorted(self.traces.traces.values(), key=lambda t: t["trace_id"])
        if not traces:
            return {"nodes": []}
        import numpy as np
        vectors = _standardize([_feature_vector(t) for t in traces])
        matrix = np.asarray(vectors)
        _, _, vh = np.linalg.svd(matrix, full_matrices=False)
        coords = matrix @ vh[:2].T
        clusters = _kmeans(vectors, min(5, len(traces)))
        return {"nodes": [{"trace_id": t["trace_id"], "x": float(coords[i, 0]),
                           "y": float(coords[i, 1]) if coords.shape[1] > 1 else 0, "cluster": clusters[i], "meta": t["meta"]}
                          for i, t in enumerate(traces)]}
