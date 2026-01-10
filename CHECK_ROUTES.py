#!/usr/bin/env python3
"""
Check available routes in FastAPI app
"""

from main import app

print("AVAILABLE ROUTES:")
print("="*50)

for route in app.routes:
    if hasattr(route, 'path') and not route.path.startswith('/docs') and not route.path.startswith('/openapi'):
        methods = list(route.methods) if route.methods else ['GET']
        method = methods[0] if methods else 'GET'
        print(f"  {method:6} {route.path}")

print("="*50)
