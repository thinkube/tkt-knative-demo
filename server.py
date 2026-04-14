"""
Knative Demo Service — minimal scale-to-zero test application.
Verifies Knative deployment, autoscaling, and health endpoints.
"""

import os
import time
import json
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

APP_NAME = os.environ.get("APP_NAME", "app-name")
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "")
AUTHOR = os.environ.get("AUTHOR_NAME", "")

GREETING = os.environ.get("GREETING", "Hello from Knative!")
SIMULATE_WORK_MS = int(os.environ.get("SIMULATE_WORK_MS", "100"))

# Track requests for observability
start_time = datetime.now(timezone.utc)
request_count = 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global request_count
        request_count += 1

        if self.path == "/health":
            self._send_json(200, {
                "status": "healthy",
                "app": APP_NAME,
                "uptime_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
                "requests_served": request_count,
            })
        elif self.path == "/":
            # Simulate processing work
            if SIMULATE_WORK_MS > 0:
                time.sleep(SIMULATE_WORK_MS / 1000.0)

            self._send_json(200, {
                "message": GREETING,
                "app": APP_NAME,
                "description": APP_DESCRIPTION,
                "author": AUTHOR,
                "request_number": request_count,
                "simulated_work_ms": SIMULATE_WORK_MS,
                "pod_start_time": start_time.isoformat(),
                "hostname": os.environ.get("HOSTNAME", "unknown"),
            })
        elif self.path == "/scale-test":
            # Endpoint for load testing — holds connection for SIMULATE_WORK_MS
            if SIMULATE_WORK_MS > 0:
                time.sleep(SIMULATE_WORK_MS / 1000.0)
            self._send_json(200, {
                "status": "completed",
                "work_ms": SIMULATE_WORK_MS,
                "request_number": request_count,
                "hostname": os.environ.get("HOSTNAME", "unknown"),
            })
        else:
            self._send_json(404, {"error": "not found"})

    def _send_json(self, status, data):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Structured log output
        print(f"[{datetime.now(timezone.utc).isoformat()}] {self.address_string()} {format % args}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("", port), Handler)
    print(f"Knative Demo '{APP_NAME}' starting on port {port}")
    print(f"  Greeting: {GREETING}")
    print(f"  Simulated work: {SIMULATE_WORK_MS}ms")
    server.serve_forever()
