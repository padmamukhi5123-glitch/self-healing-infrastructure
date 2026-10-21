#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_error(404)
            return

        result = subprocess.run(
            ["curl", "-fsS", "--max-time", "2", "http://127.0.0.1:8080/"],
            capture_output=True,
            timeout=3
        )

        healthy = 1 if result.returncode == 0 else 0

        body = (
            "# HELP self_healing_service_up Whether the web service is healthy\n"
            "# TYPE self_healing_service_up gauge\n"
            f"self_healing_service_up {healthy}\n"
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, fmt, *args):
        pass

HTTPServer(("0.0.0.0", 9101), MetricsHandler).serve_forever()
