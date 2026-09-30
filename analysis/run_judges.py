"""Homework 5 export, split, development, and held-out test workflow.

The selected mode is ``unsolicited_internal_policy_identifiers``.  HW4 stores
1 for failure present; HW5 stores 1 for Pass (failure absent) and 0 for Fail
(failure present).  This module keeps the two conventions explicit.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

from analysis.helpers import (
    freeze_judge,
    judge_alignment,
    register_judge,
    run_judge,
    split_labels,
)
from analysis.review_app.data import adapt

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "analysis" / "state"
REPORT = ROOT / "analysis" / "report"
MODE = "unsolicited_internal_policy_identifiers"
DEFAULT_TRACE_SOURCE = ROOT / "traces" / "support_traces.json"
POLICY_CONTEXT = (
    "RESP-1: Explain policies in plain language to shoppers and merchants; "
    "do not show raw policy identifiers unless the user explicitly requests "
    "them. Internal support-facing responses retain policy-identifier citations."
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _current_rows(path: Path) -> list[dict[str, Any]]:
    """Collapse an append-only label log to one current row per trace."""
    live: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("superseded_by"):
            continue
        live[str(row["trace_id"])] = row
    return list(live.values())


def _source_records(source: Path = DEFAULT_TRACE_SOURCE) -> list[dict[str, Any]]:
    raw = _read_json(source)
    rows = raw.get("traces", raw) if isinstance(raw, dict) else raw
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"trace source is empty or invalid: {source}")
    return rows


def _representative_ids(
    label_rows: list[dict[str, Any]], source: Path = DEFAULT_TRACE_SOURCE
) -> set[str]:
    """Keep one complete conversation from each close scenario-variant group."""
    labels = {str(row["trace_id"]): row for row in label_rows}
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in _source_records(source):
        trace = adapt(raw)
        if trace["trace_id"] not in labels:
            continue
        scenario = str(trace["meta"].get("scenario_id") or trace["trace_id"])
        candidates[scenario].append(trace)

    selected: set[str] = set()
    for traces in candidates.values():
        # Prefer a completed run, then richer evidence, then the latest run.
        chosen = max(
            traces,
            key=lambda trace: (
                int(trace.get("has_reply", False)),
                len(trace.get("trace", [])),
                trace.get("timestamp") or "",
                trace["trace_id"],
            ),
        )
        selected.add(chosen["trace_id"])
    return selected


def export_hw5_labels(mode: str = MODE, source: Path = DEFAULT_TRACE_SOURCE) -> Path:
    """Export independent HW4 judgments using the HW5 Pass-positive convention."""
    src = STATE / "labels" / f"{mode}.jsonl"
    dst = STATE / "hw5_labels" / f"{mode}.jsonl"
    if dst.exists():
        raise FileExistsError(
            f"{dst} already exists; preserve it because later human labels may have been appended"
        )
    hw4_rows = _current_rows(src)
    eligible = _representative_ids(hw4_rows, source)
    exported = []
    for row in sorted(hw4_rows, key=lambda item: str(item["trace_id"])):
        if str(row["trace_id"]) not in eligible:
            continue
        exported.append(
            {
                "trace_id": str(row["trace_id"]),
                "mode": mode,
                "label": 1 - int(row["label"]),
                "label_name": "Pass" if int(row["label"]) == 0 else "Fail",
                "source": "human",
                "evidence": row.get("evidence", ""),
                "hw4_label_id": row.get("id"),
            }
        )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in exported),
        encoding="utf-8",
    )
    return dst


def prepare_inputs(
    mode: str = MODE, source: Path = DEFAULT_TRACE_SOURCE
) -> list[dict[str, Any]]:
    """Save the exact, label-free trace records used by every judge version."""
    label_path = STATE / "hw5_labels" / f"{mode}.jsonl"
    labels = _current_rows(label_path)
    label_ids = {str(row["trace_id"]) for row in labels}
    by_id: dict[str, dict[str, Any]] = {}
    for raw in _source_records(source):
        trace = adapt(raw)
        by_id[trace["trace_id"]] = trace
    missing = label_ids - set(by_id)
    if missing:
        raise ValueError(f"labeled traces missing from source: {sorted(missing)[:5]}")

    records = []
    for trace_id in sorted(label_ids):
        trace = by_id[trace_id]
        role = trace.get("meta", {}).get("role") or "unknown"
        messages = [
            {"role": "context", "text": f"Caller role: {role}."},
            {"role": "policy", "text": POLICY_CONTEXT},
            *trace["trace"],
        ]
        records.append({"trace_id": trace_id, "trace": messages})
    _write_json(STATE / "hw5_trace_inputs.json", records)
    return records


def split_data(mode: str = MODE) -> dict[str, list[str]]:
    """Create the assignment's fixed 20/40/40 stratified split once."""
    input_path = STATE / "hw5_trace_inputs.json"
    records = _read_json(input_path)
    labels = _current_rows(STATE / "hw5_labels" / f"{mode}.jsonl")
    counts = {
        label: sum(int(row["label"]) == label for row in labels)
        for label in (0, 1)
    }
    if counts[0] < 30 or counts[1] < 30:
        raise ValueError(
            "HW5 requires at least 30 Pass and 30 Fail labels before splitting; "
            f"found Pass={counts[1]}, Fail={counts[0]}"
        )
    return split_labels(
        mode,
        fractions=(0.20, 0.40, 0.40),
        seed=7,
        min_per_class=10,
        eligible_trace_ids=[record["trace_id"] for record in records],
    )


def run_development(mode: str, prompt_path: str | Path) -> dict[str, Any]:
    """Register one prompt version, run only development traces, and save metrics."""
    os.environ.setdefault(
        "CARTWHEEL_JUDGE_TRACE_SOURCE", str(STATE / "hw5_trace_inputs.json")
    )
    prompt = Path(prompt_path)
    record = register_judge(
        mode=mode,
        prompt_text=prompt.read_text(encoding="utf-8"),
        judge_model="gpt-4o-mini",
    )
    judge_id = record["judge_id"]
    run_judge(judge_id, split="dev", batch_size=10)
    metrics = judge_alignment(judge_id, split="dev")
    _write_json(REPORT / f"dev-{judge_id}.json", metrics)
    return {"judge_id": judge_id, "metrics": metrics}


def run_test(judge_id: str) -> dict[str, Any]:
    """Freeze the selected version, run held-out test once, and save metrics."""
    os.environ.setdefault(
        "CARTWHEEL_JUDGE_TRACE_SOURCE", str(STATE / "hw5_trace_inputs.json")
    )
    freeze_judge(judge_id)
    run_judge(judge_id, split="test", batch_size=10)
    metrics = judge_alignment(judge_id, split="test")
    _write_json(REPORT / f"test-{judge_id}.json", metrics)
    return metrics


def status(mode: str = MODE) -> dict[str, Any]:
    label_path = STATE / "hw5_labels" / f"{mode}.jsonl"
    rows = _current_rows(label_path) if label_path.exists() else []
    passes = sum(int(row["label"]) == 1 for row in rows)
    fails = sum(int(row["label"]) == 0 for row in rows)
    return {"mode": mode, "total": len(rows), "Pass": passes, "Fail": fails}


def main() -> None:
    from observability.instrument import load_env

    load_env()
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("export-labels")
    sub.add_parser("prepare-inputs")
    sub.add_parser("split")
    sub.add_parser("status")
    dev = sub.add_parser("dev")
    dev.add_argument("prompt_path", type=Path)
    test = sub.add_parser("test")
    test.add_argument("judge_id")
    args = parser.parse_args()

    if args.command == "export-labels":
        print(export_hw5_labels())
    elif args.command == "prepare-inputs":
        print(json.dumps({"records": len(prepare_inputs())}))
    elif args.command == "split":
        print(json.dumps(split_data(), indent=2))
    elif args.command == "status":
        print(json.dumps(status(), indent=2))
    elif args.command == "dev":
        if not os.environ.get("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY is not configured; no paid batch was started")
        print(json.dumps(run_development(MODE, args.prompt_path), indent=2))
    elif args.command == "test":
        if not os.environ.get("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY is not configured; no paid batch was started")
        print(json.dumps(run_test(args.judge_id), indent=2))


if __name__ == "__main__":
    main()
