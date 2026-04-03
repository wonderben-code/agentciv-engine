#!/usr/bin/env python3
"""
REST API server using Python's built-in http.server module.
Provides /hello and /status endpoints with JSON responses and proper error handling.
"""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Record the time the server module was loaded (used for uptime calculation)
_START_TIME = time.time()

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080


class APIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the REST API."""

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def do_GET(self):
        """Dispatch GET requests to the appropriate handler."""
        routes = {
            "/hello": self._handle_hello,
            "/status": self._handle_status,
        }
        handler = routes.get(self.path)
        if handler:
            try:
                handler()
            except Exception as exc:  # pragma: no cover
                self._send_json(500, {"error": f"Internal server error: {exc}"})
        else:
            self._send_json(404, {"error": f"Not found: {self.path}"})

    # ------------------------------------------------------------------
    # Endpoint handlers
    # ------------------------------------------------------------------

    def _handle_hello(self):
        """Return a friendly greeting with a timestamp."""
        payload = {
            "message": "Hello, World!",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        self._send_json(200, payload)

    def _handle_status(self):
        """Return server status and uptime information."""
        payload = {
            "status": "ok",
            "uptime_seconds": round(time.time() - _START_TIME, 2),
        }
        self._send_json(200, payload)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _send_json(self, status_code: int, data: dict):
        """Serialise *data* to JSON and write a complete HTTP response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # noqa: D102
        """Override to use a cleaner log format."""
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {fmt % args}")


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    """Start the HTTP server and block until interrupted."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"REST API server listening on http://{host}:{port}")
    print("Endpoints: GET /hello  |  GET /status")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run()
