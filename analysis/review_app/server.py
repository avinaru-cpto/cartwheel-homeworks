"""Local HTTP server for the custom HW4 review workspace."""
from __future__ import annotations

import argparse
import hmac
import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from analysis.helpers import _state
from .data import LangfuseBridge, ROOT, SourceError, load_store
from .state import Conflict, ReviewState

UI = Path(__file__).with_name("index.html")


def make_server(state: ReviewState, host="127.0.0.1", port=8021):
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, data, status=200, content_type="application/json; charset=utf-8"):
            content = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(content)

        def valid_host(self):
            authority = urlparse("http://" + self.headers.get("Host", ""))
            try:
                return authority.hostname in {"localhost", "127.0.0.1", "::1"} and authority.port == self.server.server_port
            except ValueError:
                return False

        def do_GET(self):
            if not self.valid_host():
                return self.send({"error": "Use the local review URL."}, 403)
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            try:
                if parsed.path in {"/", "/index.html"}:
                    return self.send(UI.read_bytes(), content_type="text/html; charset=utf-8")
                if parsed.path == "/api/state":
                    return self.send({**state.snapshot(), "csrf_token": token})
                if parsed.path == "/api/revision":
                    return self.send({"revision": state.revision()})
                if parsed.path == "/api/session":
                    session = query.get("id", [""])[0]
                    if session not in state.traces.sessions:
                        return self.send({"error": "Session not found."}, 404)
                    return self.send({"session_id": session, "traces": state.traces.sessions[session]})
                if parsed.path == "/api/raw":
                    tid = query.get("id", [""])[0]
                    state.require_trace(tid)
                    return self.send(state.traces.raw[tid])
                if parsed.path == "/api/graph":
                    return self.send(state.graph())
                if parsed.path == "/api/spec":
                    return self.send({"text": (ROOT / "SPEC.md").read_text()})
                return self.send({"error": "Not found."}, 404)
            except (ValueError, TypeError, KeyError):
                return self.send({"error": "Invalid source or state file. Inspect the saved JSON before continuing."}, 422)
            except OSError:
                return self.send({"error": "Could not read the local files."}, 500)

        def do_POST(self):
            origin = self.headers.get("Origin")
            if not self.valid_host() or (origin and urlparse(origin).netloc != self.headers.get("Host")):
                return self.send({"error": "Cross-origin writes are not allowed."}, 403)
            if not hmac.compare_digest(self.headers.get("X-Review-Token", ""), token):
                return self.send({"error": "Refresh the app before saving."}, 403)
            if self.headers.get_content_type() != "application/json":
                return self.send({"error": "Send JSON."}, 415)
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 1000000:
                    return self.send({"error": "Request size is invalid."}, 413)
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError("Expected a JSON object.")
                route = urlparse(self.path).path
                if not route.startswith("/api/"):
                    return self.send({"error": "Not found."}, 404)
                result = state.mutate(route.removeprefix("/api/"), body)
                return self.send(result)
            except Conflict as exc:
                return self.send({"error": str(exc)}, 409)
            except (ValueError, KeyError, TypeError) as exc:
                return self.send({"error": str(exc)}, 422)
            except OSError:
                return self.send({"error": "Save failed. Your browser draft remains available."}, 500)

    return ThreadingHTTPServer((host, port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8021)
    parser.add_argument("--source", default="langfuse", help="langfuse (default) or an offline export path")
    parser.add_argument("--offline-reason", default="")
    parser.add_argument("--state-dir", type=Path, default=_state.state_root())
    args = parser.parse_args()
    from observability.instrument import load_env
    load_env()
    bridge = LangfuseBridge()
    print("Loading the review source; no model calls or judgments are made.", flush=True)
    try:
        traces = load_store(args.source, bridge, args.offline_reason)
    except (SourceError, ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\nIf Langfuse is unavailable, pass --source traces/support_traces.json --offline-reason 'reason'.\n")
    state = ReviewState(args.state_dir.resolve(), traces, bridge)
    # One writer process per state directory. Multiple browser tabs use the
    # state revision to reject stale updates instead of overwriting each other.
    import fcntl
    import tempfile
    import hashlib
    lock_name = hashlib.sha256(str(state.root).encode()).hexdigest()
    with (Path(tempfile.gettempdir()) / ("cartwheel-review-" + lock_name + ".lock")).open("w") as lock_file:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.exit(1, "Another review server is already using this state directory.\n")
        server = make_server(state, port=args.port)
        print(f"Review workspace: http://127.0.0.1:{args.port}", flush=True)
        print(f"{len(traces.traces)} distinct traces · {len(traces.sessions)} sessions · {traces.source['kind']}", flush=True)
        print(f"State: {state.root}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == "__main__":
    main()
