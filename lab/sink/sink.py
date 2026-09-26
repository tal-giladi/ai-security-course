"""Local egress sink for the security lab.

Where "exfiltration" goes in every offensive lab — NEVER the internet (lab/README.md safety
model). It is a tiny stdlib HTTP server that records every request it receives (method, path,
query, headers, body) to an in-memory log and to `sink_log.jsonl`, so a lab can *measure*
whether a synthetic canary reached an attacker-controlled endpoint, with zero real data leaving
the machine.

Run:  py lab/sink/sink.py            # listens on 127.0.0.1:8888 only
Then point any lab "attacker endpoint" at http://127.0.0.1:8888/collect?d=<payload>.

Inspect programmatically via the SinkLog class, or read sink_log.jsonl.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

LOG_PATH = Path(__file__).with_name("sink_log.jsonl")
CANARY = re.compile(r"LAB-CANARY-[\w-]+")


class SinkLog:
    """Read/inspect what the sink captured (used by labs to assert exfiltration)."""

    def __init__(self, path: Path = LOG_PATH):
        self.path = path

    def entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(l) for l in self.path.read_text(encoding="utf-8").splitlines() if l.strip()]

    def canaries_received(self) -> set[str]:
        found = set()
        for e in self.entries():
            blob = json.dumps(e)
            found.update(CANARY.findall(blob))
        return found

    def clear(self):
        self.path.write_text("", encoding="utf-8")


class _Handler(BaseHTTPRequestHandler):
    def _record(self, method: str):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length).decode("latin-1", "ignore") if length else ""
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "method": method,
            "path": parsed.path,
            "query": parse_qs(parsed.query),
            "headers": {k: v for k, v in self.headers.items()},
            "body": body,
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        hit = CANARY.findall(json.dumps(entry))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "canaries_seen": hit}).encode())

    def do_GET(self):  self._record("GET")
    def do_POST(self): self._record("POST")

    def log_message(self, *a):  # quiet
        pass


def serve(host: str = "127.0.0.1", port: int = 8888):
    server = ThreadingHTTPServer((host, port), _Handler)
    print(f"[sink] listening on http://{host}:{port}  (logging to {LOG_PATH})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[sink] stopped")


if __name__ == "__main__":
    serve()
