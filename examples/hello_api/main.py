#!/usr/bin/env python3
"""
Main entry point for the REST API project.
Starts the HTTP server defined in server.py.
"""

from server import run


def main():
    """Start the REST API server."""
    run()


if __name__ == "__main__":
    main()
