#!/usr/bin/env python3
import json
import logging
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

PLAYBOOK = "/home/ubuntu/self-healing-infrastructure/ansible/recover_service.yml"
LOG_FILE = "/home/ubuntu/self-healing-infrastructure/logs/webhook.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

class AlertHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/alerts":
            self.send_error(404)
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 1_000_000:
                self.send_error(400, "Invalid payload size")
                return

            payload = json.loads(self.rfile.read(size))
            alerts = payload.get("alerts", [])

            service_alert = any(
                alert.get("status") == "firing"
                and alert.get("labels", {}).get("alertname") == "ServiceDown"
                for alert in alerts
            )

            if not service_alert:
                logging.info("Alert received; no ServiceDown recovery required.")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Alert received")
                return

            result = subprocess.run(
                ["/usr/bin/sudo", "-n", "/usr/bin/ansible-playbook", PLAYBOOK],
                capture_output=True,
                text=True,
                timeout=60
            )

            logging.info("Ansible exit code: %s", result.returncode)
            logging.info("Ansible output: %s", result.stdout[-4000:])
            if result.stderr:
                logging.error("Ansible error: %s", result.stderr[-2000:])

            self.send_response(200 if result.returncode == 0 else 500)
            self.end_headers()
            self.wfile.write(
                b"Recovery completed" if result.returncode == 0
                else b"Recovery failed"
            )

        except Exception:
            logging.exception("Webhook processing failed")
            self.send_error(500, "Webhook processing failed")

    def log_message(self, fmt, *args):
        logging.info("HTTP " + fmt, *args)

HTTPServer(("0.0.0.0", 5001), AlertHandler).serve_forever()
