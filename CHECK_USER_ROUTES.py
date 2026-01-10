#!/usr/bin/env python3
"""
Check user-related routes
"""

from main import app

print("USER-RELATED ROUTES:")
print("="*50)

for route in app.routes:
    if hasattr(route, 'path'):
        path = route.path.lower()
        if 'me' in path or 'user' in path:
            methods = list(route.methods) if route.methods else ['GET']
            method = methods[0] if methods else 'GET'
            print(f"  {method:6} {route.path}")

print("="*50)
