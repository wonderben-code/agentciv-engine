#!/usr/bin/env python3
"""
Tests for the REST API server.
"""
import json
import threading
import time
import urllib.request
import urllib.error
import unittest


class TestServer(unittest.TestCase):
    BASE_URL = "http://localhost:8080"

    def _get(self, path):
        url = self.BASE_URL + path
        with urllib.request.urlopen(url) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, resp.headers.get("Content-Type"), json.loads(body)

    def _get_raw(self, path):
        url = self.BASE_URL + path
        try:
            with urllib.request.urlopen(url) as resp:
                body = resp.read().decode("utf-8")
                return resp.status, resp.headers.get("Content-Type"), body
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            return e.code, e.headers.get("Content-Type"), body

    def test_hello_endpoint(self):
        status, content_type, data = self._get("/hello")
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Hello, World!")

    def test_status_endpoint(self):
        status, content_type, data = self._get("/status")
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "ok")
        self.assertIn("uptime_seconds", data)

    def test_404_returns_json(self):
        status, content_type, body = self._get_raw("/nonexistent")
        self.assertEqual(status, 404)
        self.assertIn("application/json", content_type)
        data = json.loads(body)
        self.assertIn("error", data)

    def test_hello_has_timestamp(self):
        _, _, data = self._get("/hello")
        self.assertIn("timestamp", data)


if __name__ == "__main__":
    unittest.main()
