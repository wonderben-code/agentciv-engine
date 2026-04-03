#!/usr/bin/env python3
"""
api_server.py — public entry point for the REST API.

Re-exports the core components from server.py so that callers can use
either module interchangeably:

    from api_server import run, APIHandler

Endpoints
---------
GET /hello  → 200 JSON  {"message": "Hello, World!", "timestamp": "..."}
GET /status → 200 JSON  {"status": "ok", "uptime_seconds": <float>}
<other>     → 404 JSON  {"error": "Not found: <path>"}
"""

from server import APIHandler, run, DEFAULT_HOST, DEFAULT_PORT  # noqa: F401

__all__ = ["APIHandler", "run", "DEFAULT_HOST", "DEFAULT_PORT"]

if __name__ == "__main__":
    run()
