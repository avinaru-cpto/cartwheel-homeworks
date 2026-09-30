"""Disposable browser-QA server. Never reads .env or actual homework state.

Run: uv run python -m tests.review_app_fixture
All observations and modes are synthetic test fixtures, not homework labels.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import re

from analysis.review_app.data import TraceStore
from analysis.review_app.server import UI, make_server
from analysis.review_app.state import ReviewState
from tests.test_review_app import final_mode, raw_trace


def main():
    rows = [raw_trace(i, session="multi-turn-fixture" if i in (6, 7) else None) for i in range(30)]
    rows[7]["trace"][0]["text"] = "Synthetic follow-up: use the corrected order ID."
    rows[6]["trace"][2]["content"]["retrieval"] = [{"policy_id": "fixture-policy", "body": "Synthetic policy text for browser QA. " * 30}]
    rows[8]["trace"][0]["text"] = '<script>alert("untrusted trace")</script> is literal test data.'
    rows[9]["trace"][3]["text"] = (
        "# Order status\n\nYour **order** is delivered.\n\n"
        "- **Total:** $42.00\n- Quantity: 1\n\n"
        "| Event | Date |\n|---|---|\n| Ordered | 2026-06-20 |\n| Delivered | 2026-06-24 |\n\n"
        "> This is a synthetic quotation.\n\n"
        "Use `refund_eligible` only when needed. See [policy](https://example.org/policy)."
    )
    store = TraceStore(rows, {"kind": "offline", "description": "SYNTHETIC BROWSER QA",
                              "reason": "Disposable synthetic fixtures; these are not homework judgments.",
                              "loaded_at": "2026-07-01T12:00:00Z"})
    with TemporaryDirectory(prefix="cartwheel-review-qa-") as directory:
        state = ReviewState(Path(directory), store)
        final_mode(state)
        state.write("sample_manifest.json", {"version": 1, "batches": [{"name": "uniform_initial", "count": 15}],
                                              "samples": [{"trace_id": f"{i:032x}", "session_id": store.traces[f"{i:032x}"]["session_id"], "batch": "uniform_initial"} for i in range(15)]})
        state.write("suggestions.json", [{"id": "synthetic-suggestion", "trace_id": f"{0:032x}", "mode": "test_mode", "quote": "placed", "idx": 3}])
        quote = "- **Total:** $42.00"
        start = rows[9]["trace"][3]["text"].index(quote)
        state.mutate("annotation", {"revision": state.revision(), "id": "legacy-markdown-note",
                                     "trace_id": f"{9:032x}", "kind": "first_failure", "idx": 3,
                                     "quote": quote, "start": start, "end": start + len(quote),
                                     "note": "Synthetic legacy annotation: keep this source anchor unchanged."})
        server = make_server(state, port=8022)
        base_handler = server.RequestHandlerClass

        class QAHandler(base_handler):
            def do_GET(self):
                if self.path == "/markdown-checks" and self.valid_host():
                    renderer = re.search(r'<script id="review-markdown">[\s\S]*?</script>', UI.read_text()).group()
                    page = Path(__file__).with_name("review_markdown_browser.html").read_text()
                    return self.send(page.replace("<!--RENDERER-->", renderer).encode(),
                                     content_type="text/html; charset=utf-8")
                return super().do_GET()

        server.RequestHandlerClass = QAHandler
        print(f"Synthetic QA only: http://127.0.0.1:8022 · temporary state: {directory}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == "__main__":
    main()
