#!/usr/bin/env python3
"""
Simple test script to check if routes are properly registered
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from src.main import app

def test_routes():
    print("Available routes:")
    for route in app.routes:
        print(f"- {route.methods} {route.path}")

    print("\nOpenAPI schema paths:")
    openapi_schema = app.openapi()
    for path, methods in openapi_schema.get("paths", {}).items():
        print(f"- {path}: {list(methods.keys())}")

if __name__ == "__main__":
    test_routes()