"""HW4 interface checks: synthetic evidence, temporary state, no model calls."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from analysis.review_app.data import LangfuseBridge, SourceError, TraceStore, adapt
from analysis.review_app.state import Conflict, ReviewState, mode_revision


def raw_trace(i=0, *, session=None, timestamp=None):
    return {
        "id": f"{i:032x}", "timestamp": timestamp or f"2026-07-01T12:{i % 60:02d}:00Z",
        "metadata": {"attributes": {"cartwheel.session_id": session or f"session-{i}",
                                      "cartwheel.scenario_id": f"scenario-{i // 2}",
                                      "cartwheel.user_role": ["shopper", "merchant", "support"][i % 3]}},
        "trace": [{"role": "user", "text": f"Synthetic fixture {i}: check my order."},
                  {"role": "tool_call", "name": "get_order", "arguments": {"order_id": i}},
                  {"role": "tool_result", "name": "get_order", "content": {"ok": True, "status": "placed"}},
                  {"role": "assistant", "text": "The recorded status is placed."}],
        "features": {"tokens": 100 + i * 37},
    }


@pytest.fixture
def review(tmp_path):
    store = TraceStore([raw_trace(i) for i in range(150)], {"kind": "offline", "description": "Synthetic fixture", "reason": "Offline test", "loaded_at": "2026-07-01"})
    return ReviewState(tmp_path, store)


def mutate(state, action, **body):
    return state.mutate(action, {"revision": state.revision(), **body})["result"]


def note(state, i, kind="no_failure"):
    return mutate(state, "annotation", trace_id=f"{i:032x}", note="Synthetic reviewer observation", kind=kind)


def final_mode(state, name="test_mode"):
    observations = [note(state, i, "first_failure" if i < 3 else "no_failure") for i in range(6)]
    mode = {"name": name, "definition": "The trace violates the synthetic fixture rule.", "status": "final",
            "boundary": "Other synthetic fixture rules are excluded.", "requirement_source": "RESP-2",
            "evaluator_type": "code", "created_from": [o["id"] for o in observations[:3]],
            "example_trace_ids": [f"{i:032x}" for i in range(3)],
            "close_negative_trace_ids": [f"{i:032x}" for i in range(3, 6)]}
    return mutate(state, "mode", mode=mode, human_confirmed=True)


def test_sessions_preserve_retry_ids_and_sort_true_time():
    first = raw_trace(1, session="shared", timestamp="2026-07-01T09:00:00+02:00")
    second = raw_trace(2, session="shared", timestamp="2026-07-01T08:00:00Z")
    retry = raw_trace(3, session="other", timestamp="2026-07-01T08:01:00Z")
    for r in (first, second, retry):
        r["metadata"]["attributes"]["cartwheel.scenario_id"] = "same-scenario"
    store = TraceStore([second, first, retry], {"kind": "offline"})
    assert len(store.traces) == 3
    assert [t["trace_id"] for t in store.sessions["shared"]] == [first["id"], second["id"]]
    assert len(store.sessions) == 2


def test_missing_sessions_do_not_collapse_and_conflicting_ids_fail():
    a, b = raw_trace(1), raw_trace(2)
    a["metadata"] = b["metadata"] = {}
    assert len(TraceStore([a, b], {}).sessions) == 2
    with pytest.raises(ValueError, match="Conflicting"):
        TraceStore([a, {**a, "output": "different"}], {})


def test_system_context_diagnostics_and_raw_activity_are_retained():
    raw = raw_trace()
    raw["observations"] = [{"id": "obs", "type": "GENERATION", "level": "ERROR", "statusMessage": "Synthetic provider error",
                            "input": {"messages": [{"role": "system", "parts": [{"type": "text", "content": "Synthetic system context"}]}]}}]
    t = adapt(raw)
    assert t["diagnostics"][0]["statusMessage"] == "Synthetic provider error"
    assert t["system_messages"][0]["role"] == "system"
    assert t["trace_id"] == raw["id"]


def test_store_scope_comes_from_tool_attributes_not_order_content():
    raw = raw_trace()
    raw["observations"] = [{"type": "TOOL", "name": "get_order", "metadata": {"attributes": {"cartwheel.store_id": "19"}}}]
    assert adapt(raw)["meta"]["store"] == "19"
    raw["observations"].append({"type": "TOOL", "metadata": {"attributes": {"cartwheel.store_id": "1"}}})
    assert "store" not in adapt(raw)["meta"]


def test_snapshot_does_not_write_or_count_unreviewed_as_absent(review):
    assert review.snapshot()["progress"]["reviewed"] == 0
    assert list(review.root.iterdir()) == []
    assert review.labels() == []


def test_note_quote_roundtrip_history_and_safe_delete(review):
    t = f"{0:032x}"
    review.write("annotations.json", {"annotations": [], "keep_me": "existing metadata"})
    a = mutate(review, "annotation", trace_id=t, kind="first_failure", idx=3, quote="recorded status", start=4, end=19, note="Synthetic first observation")
    mutate(review, "annotation", **{**a, "note": "Synthetic revised observation"})
    current = review.active_annotations()[0]
    assert current["history"][0]["note"] == "Synthetic first observation"
    mutate(review, "annotation", **{**current, "delete": True})
    assert review.active_annotations() == []
    assert review.read("annotations.json", {})["keep_me"] == "existing metadata"
    assert len(review.annotations()[0]["history"]) == 2


@pytest.mark.parametrize("extra", [{"mode": "some_mode"}, {"label": 0}, {"idx": 99}, {"idx": 3, "quote": "fabricated quote"}])
def test_open_coding_rejects_modes_invalid_steps_and_fabricated_evidence(review, extra):
    with pytest.raises(ValueError):
        mutate(review, "annotation", trace_id=f"{0:032x}", note="test", **extra)
    assert review.annotations() == []


def test_stale_revision_and_duplicate_initial_review_are_rejected(review):
    revision = review.revision()
    note(review, 0)
    with pytest.raises(Conflict):
        review.mutate("annotation", {"revision": revision, "trace_id": f"{1:032x}", "note": "stale"})
    with pytest.raises(ValueError, match="already"):
        note(review, 0)


def test_sampling_is_explicit_reproducible_and_does_not_count_context(review, tmp_path):
    mutate(review, "batch", batch="uniform_initial", seed=9)
    first = review.manifest()["samples"]
    assert len({s["trace_id"] for s in first}) == 15
    other = ReviewState(tmp_path / "other", review.traces)
    mutate(other, "batch", batch="uniform_initial", seed=9)
    assert first == other.manifest()["samples"]
    note(review, int(first[0]["trace_id"], 16))
    assert review.snapshot()["progress"]["reviewed"] == 1
    with pytest.raises(ValueError, match="already"):
        mutate(review, "batch", batch="uniform_initial")
    with pytest.raises(ValueError, match="Finish"):
        mutate(review, "batch", batch="cluster")


def test_breadth_batches_do_not_overlap(review):
    for batch in ("uniform_initial", "cluster", "dimension"):
        mutate(review, "batch", batch=batch, dimension="role")
        for s in review.manifest()["samples"]:
            if s["trace_id"] not in review.reviewed():
                note(review, int(s["trace_id"], 16))
    samples = review.manifest()["samples"]
    assert len(samples) == len({s["trace_id"] for s in samples}) == 60
    assert review.manifest()["batches"][-1]["allocation"] == {"shopper": 10, "merchant": 10, "support": 10}


def test_final_mode_requires_human_origins_and_signoff(review):
    with pytest.raises(ValueError, match="originating"):
        mutate(review, "mode", mode={"name": "unsupported_guess", "definition": "test", "status": "candidate"})
    a = note(review, 0)
    with pytest.raises(ValueError, match="three reviewed"):
        mutate(review, "mode", mode={"name": "test_mode", "definition": "test", "status": "final", "created_from": [a["id"]]})


@pytest.fixture
def ready_for_final_batch(review):
    """Synthetic completed 15+15+30+25 sample, independent of homework state."""
    samples, batches, offset = [], [], 0
    for name, count in (("uniform_initial", 15), ("cluster", 15),
                        ("dimension", 30), ("depth", 25)):
        for i in range(offset, offset + count):
            note(review, i, "first_failure" if i < 3 else "no_failure")
            samples.append({"trace_id": f"{i:032x}", "session_id": f"session-{i}", "batch": name})
        batches.append({"name": name, "count": count, "source": review.traces.source})
        offset += count
    review.write("sample_manifest.json", {"version": 1, "samples": samples, "batches": batches})
    return review


def sampling_test_mode(state, name="draft_mode", status="candidate"):
    mode = {"name": name, "definition": "Synthetic evidence-backed draft rule.",
            "status": status, "created_from": [state.active_annotations()[0]["id"]]}
    if status == "final":
        mode.update({"boundary": "Other fixture rules are excluded.",
                     "requirement_source": "RESP-2", "evaluator_type": "code",
                     "example_trace_ids": [f"{i:032x}" for i in range(3)],
                     "close_negative_trace_ids": [f"{i:032x}" for i in range(3, 6)]})
    return mutate(state, "mode", mode=mode, human_confirmed=status == "final")


@pytest.mark.parametrize("final_count,candidate_count", [(0, 1), (3, 2), (5, 0), (0, 9)])
def test_final_uniform_accepts_drafted_taxonomy_without_finalizing_modes(
        ready_for_final_batch, final_count, candidate_count):
    import random
    state = ready_for_final_batch
    for i in range(final_count + candidate_count):
        sampling_test_mode(state, f"fixture_mode_{i}", "final" if i < final_count else "candidate")
    # A context-only review must remain excluded, even outside the sample.
    note(state, 145)
    modes_before, notes_before = state.all_modes(), state.annotations()
    manifest_before = state.manifest()
    unused = sorted(set(state.traces.traces) - state.reviewed())
    mutate(state, "batch", batch="uniform_final", seed=9)
    samples = state.manifest()["samples"]
    selected = [s["trace_id"] for s in samples if s["batch"] == "uniform_final"]
    assert selected == random.Random(9).sample(unused, 15)
    assert len(samples) == len({s["trace_id"] for s in samples}) == 100
    assert samples[:85] == manifest_before["samples"]
    assert not set(selected) & state.reviewed()
    assert state.all_modes() == modes_before
    assert state.annotations() == notes_before
    assert state.labels() == []
    assert state.snapshot()["progress"]["final_modes"] == final_count
    assert state.snapshot()["progress"]["reviewed"] == 85
    taxonomy = state.manifest()["batches"][-1]["taxonomy_at_selection"]
    assert taxonomy == [{"name": m["name"], "status": m["status"],
                         "definition": m["definition"], "revision": mode_revision(m)} for m in modes_before]
    with pytest.raises(ValueError, match="already recorded"):
        mutate(state, "batch", batch="uniform_final", seed=10)


@pytest.mark.parametrize("only_retired", [False, True])
def test_final_uniform_still_requires_an_active_taxonomy(ready_for_final_batch, only_retired):
    state = ready_for_final_batch
    if only_retired:
        sampling_test_mode(state, status="retired")
    revision = state.revision()
    with pytest.raises(ValueError, match="Draft a taxonomy"):
        mutate(state, "batch", batch="uniform_final")
    assert state.revision() == revision


def test_final_uniform_still_requires_all_earlier_reviews(ready_for_final_batch):
    state = ready_for_final_batch
    sampling_test_mode(state)
    last_note = state.active_annotations()[-1]
    mutate(state, "annotation", **{**last_note, "delete": True})
    revision = state.revision()
    with pytest.raises(ValueError, match="Finish the depth"):
        mutate(state, "batch", batch="uniform_final")
    assert state.revision() == revision


def test_final_sampling_does_not_relax_mode_evidence_or_human_signoff(ready_for_final_batch):
    state = ready_for_final_batch
    candidate = sampling_test_mode(state)
    mutate(state, "batch", batch="uniform_final")
    with pytest.raises(ValueError, match="three reviewed, human-confirmed positive"):
        mutate(state, "mode", mode={**candidate, "status": "final"},
               reason="Synthetic attempt without evidence", human_confirmed=True)
    complete = {**candidate, "status": "final", "boundary": "Synthetic boundary",
                "requirement_source": "RESP-2", "evaluator_type": "code",
                "example_trace_ids": [f"{i:032x}" for i in range(3)],
                "close_negative_trace_ids": [f"{i:032x}" for i in range(3, 6)]}
    with pytest.raises(ValueError, match="explicit human confirmation"):
        mutate(state, "mode", mode=complete, reason="Synthetic attempt without signoff")
    assert state.all_modes()[0]["status"] == "candidate"
    assert state.labels() == []


def test_labels_require_final_mode_review_and_evidence(review):
    with pytest.raises(ValueError, match="finalized"):
        mutate(review, "label", mode="unknown", trace_id=f"{0:032x}", label=0, evidence="Test")
    final_mode(review)
    with pytest.raises(ValueError, match="initial"):
        mutate(review, "label", mode="test_mode", trace_id=f"{40:032x}", label=0, evidence="Test")
    with pytest.raises(ValueError, match="evidence"):
        mutate(review, "label", mode="test_mode", trace_id=f"{0:032x}", label=0, evidence="")
    with pytest.raises(ValueError, match="Choose present"):
        mutate(review, "label", mode="test_mode", trace_id=f"{0:032x}", label=False, evidence="Test")


def test_label_flip_is_auditable_and_retry_identity_stable(review):
    final_mode(review)
    first = mutate(review, "label", mode="test_mode", trace_id=f"{0:032x}", label=1, evidence="Synthetic positive")
    second = mutate(review, "label", mode="test_mode", trace_id=f"{0:032x}", label=0, evidence="Synthetic correction")
    assert first["score_id"] == second["score_id"]
    assert first["score_timestamp"] == second["score_timestamp"]
    assert second["supersedes"] == first["id"]
    assert len(review.label_rows("test_mode")) == 2
    assert review.labels()[0]["label"] == 0
    assert second["sync_status"] == "pending"


def test_mode_revisions_invalidate_old_decisions_and_keep_history(review):
    mode = final_mode(review)
    review.write("sample_manifest.json", {"samples": [{"trace_id": f"{0:032x}", "batch": "uniform_initial"}], "batches": []})
    mutate(review, "label", mode="test_mode", trace_id=f"{0:032x}", label=1, evidence="Synthetic evidence")
    assert review.snapshot()["progress"]["missing"] == 0
    mutate(review, "mode", mode={**mode, "definition": "A revised synthetic rule."}, reason="Synthetic boundary refinement", human_confirmed=True)
    assert review.snapshot()["progress"]["missing"] == 1
    assert len(review.read("patterns.json", {})["revisions"]) == 2


def test_failed_remote_write_is_durable_and_can_retry(review):
    final_mode(review)
    class Fake:
        configured = True
        failing = True
        def write_score(self, row):
            if self.failing:
                raise SourceError("Synthetic outage")
    review.bridge = Fake()
    review.traces.source["kind"] = "langfuse"
    result = mutate(review, "label", mode="test_mode", trace_id=f"{0:032x}", label=1, evidence="test")
    assert result["sync_status"] == "pending"
    review.bridge.failing = False
    assert mutate(review, "sync")["synced"] == 1
    assert review.labels()[0]["sync_status"] == "synced"


def test_suggestion_rejection_is_preserved_without_a_label(review):
    review.write("suggestions.json", [{"id": "s1", "trace_id": f"{0:032x}", "mode": "test_mode", "quote": "placed"}])
    mutate(review, "suggestion", id="s1", decision="rejected", reason="Synthetic boundary excludes this example.")
    assert review.read("suggestions.json", [])[0]["status"] == "rejected"
    assert review.labels() == []


def test_suggestion_acceptance_requires_review_and_writes_label(review):
    final_mode(review)
    review.write("suggestions.json", [{"id": "s1", "trace_id": f"{0:032x}", "mode": "test_mode", "quote": "placed", "idx": 3}])
    mutate(review, "suggestion", id="s1", decision="accepted", reason="Synthetic acceptance evidence")
    assert review.labels()[0]["source"] == "accepted_suggestion"
    assert review.read("suggestions.json", [])[0]["status"] == "accepted"
    assert len(review.active_annotations()) == 7
    assert review.active_annotations()[-1]["source"] == "accepted_suggestion"


def test_candidate_suggestion_acceptance_does_not_prematurely_label(review):
    a = note(review, 0, "first_failure")
    mutate(review, "mode", mode={"name": "test_mode", "definition": "Candidate fixture rule", "status": "candidate", "created_from": [a["id"]]})
    review.write("suggestions.json", [{"id": "candidate", "trace_id": f"{0:032x}", "mode": "test_mode", "quote": "placed", "idx": 3}])
    result = mutate(review, "suggestion", id="candidate", decision="accepted", reason="Synthetic accepted observation")
    assert result["needs_final_label"] is True
    assert review.labels() == []
    assert len(review.active_annotations()) == 2


def test_invalid_suggestion_evidence_cannot_partially_write_a_label(review):
    final_mode(review)
    review.write("suggestions.json", [{"id": "invalid", "trace_id": f"{0:032x}", "mode": "test_mode", "quote": "not in this trace", "idx": 3}])
    with pytest.raises(ValueError, match="quote"):
        mutate(review, "suggestion", id="invalid", decision="accepted", reason="Synthetic test")
    assert review.labels() == []


def test_langfuse_bridge_uses_stable_ingestion_timestamp(monkeypatch):
    bridge = LangfuseBridge()
    calls = []
    def fake(path, body=None):
        calls.append((path, body))
        if path.startswith("score-configs"):
            return {"data": [{"id": "cfg", "name": "test_mode", "dataType": "NUMERIC", "minValue": 0, "maxValue": 1}]}
        return {"successes": [{"id": "event"}], "errors": []}
    monkeypatch.setattr(bridge, "request", fake)
    bridge.write_score({"trace_id": "a"*32, "mode": "test_mode", "label": 1, "id": "revision", "score_id": "stable", "score_timestamp": "2026-07-01T01:00:00Z"})
    body = calls[-1][1]["batch"][0]["body"]
    assert body["timestamp"] == "2026-07-01T01:00:00Z"
    assert body["id"] == "stable"
    assert body["traceId"] == "a"*32
    assert body["configId"] == "cfg"


def test_projection_preserves_trace_identity(review):
    graph = review.graph()
    assert len(graph["nodes"]) == 150
    assert {n["trace_id"] for n in graph["nodes"]} == set(review.traces.traces)
    assert all(isinstance(n["x"], float) for n in graph["nodes"])


def test_langfuse_score_name_limit_is_stable_without_renaming_local_modes():
    assert LangfuseBridge.score_name("a" * 35) == "a" * 35
    name = "unsolicited_internal_policy_identifiers"
    alias = LangfuseBridge.score_name(name)
    assert len(alias) == 35
    assert alias.startswith(name[:22] + "_")
    assert alias == LangfuseBridge.score_name(name)
    assert alias != LangfuseBridge.score_name(name + "_other")


def test_long_mode_creates_bounded_config_and_matching_score(monkeypatch):
    bridge = LangfuseBridge()
    name = "unsolicited_internal_policy_identifiers"
    calls = []
    def fake(path, body=None):
        calls.append((path, body))
        if path.startswith("score-configs?"):
            return {"data": []}
        if path == "score-configs":
            assert len(body["name"]) <= 35
            return {"id": "long-mode-config"}
        return {"successes": [{"id": "event"}], "errors": []}
    monkeypatch.setattr(bridge, "request", fake)
    row = {"trace_id": "a" * 32, "mode": name, "label": 0, "id": "revision",
           "score_id": "stable", "score_timestamp": "2026-07-01T01:00:00Z"}
    bridge.write_score(row)
    config = next(body for path, body in calls if path == "score-configs")
    score = calls[-1][1]["batch"][0]["body"]
    assert config["name"] == score["name"] == row["langfuse_score_name"]
    assert name in config["description"] and name in score["comment"]
    assert row["mode"] == name and score["id"] == "stable"
    assert score["value"] == 0 and score["configId"] == "long-mode-config"
    assert score["timestamp"] == "2026-07-01T01:00:00Z"


def test_long_mode_reuses_existing_alias_config(monkeypatch):
    bridge = LangfuseBridge()
    name = "unsolicited_internal_policy_identifiers"
    calls = []
    def fake(path, body=None):
        calls.append((path, body))
        assert body is None
        return {"data": [{"id": "existing", "name": bridge.score_name(name),
                          "dataType": "NUMERIC", "minValue": 0, "maxValue": 1}]}
    monkeypatch.setattr(bridge, "request", fake)
    assert bridge.score_config(name) == "existing"
    assert bridge.score_config(name) == "existing"
    assert len(calls) == 1


def test_http_routes_csrf_and_note_persistence(review):
    from analysis.review_app.server import make_server
    import threading
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    server = make_server(review, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(base) as r:
            assert b"Review workspace" in r.read()
        with urlopen(base + "/api/state") as r:
            state = json.load(r)
        body = json.dumps({"revision": state["revision"], "trace_id": f"{0:032x}", "kind": "no_failure"}).encode()
        with pytest.raises(HTTPError) as exc:
            urlopen(Request(base + "/api/annotation", data=body, headers={"Content-Type": "application/json"}))
        assert exc.value.code == 403
        headers = {"Content-Type": "application/json", "X-Review-Token": state["csrf_token"]}
        with urlopen(Request(base + "/api/annotation", data=body, headers=headers)) as r:
            assert json.load(r)["ok"]
        with pytest.raises(HTTPError) as exc:
            urlopen(Request(base + "/api/annotation", data=body, headers={**headers, "Origin": "https://example.com"}))
        assert exc.value.code == 403
        assert review.reviewed() == {f"{0:032x}"}
    finally:
        server.shutdown()
        server.server_close()
