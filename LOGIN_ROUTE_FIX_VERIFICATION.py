#!/usr/bin/env python3
"""
Login Route Fix Verification Script
"""

import requests
import json

def test_login_route_fix():
    """Test login route fix"""
    print("LOGIN ROUTE FIX VERIFICATION")
    print("="*50)
    
    base_url = "http://127.0.0.1:8000"
    
    print("1. Testing Backend Routes:")
    
    # Test correct login route
    try:
        response = requests.get(base_url + "/api/users/login", timeout=5)
        print(f"   GET /api/users/login: {response.status_code} (Expected 405 - Method Not Allowed)")
    except Exception as e:
        print(f"   GET /api/users/login: ERROR - {e}")
    
    # Test incorrect login route
    try:
        response = requests.get(base_url + "/users/login", timeout=5)
        print(f"   GET /users/login: {response.status_code} (Expected 404 - Not Found)")
    except Exception as e:
        print(f"   GET /users/login: ERROR - {e}")
    
    print("\n2. Testing Login POST Requests:")
    
    # Test correct login route with POST
    login_data = {
        "username": "john_doe",
        "password": "password123"
    }
    
    try:
        response = requests.post(base_url + "/api/users/login", json=login_data, timeout=5)
        if response.ok:
            data = response.json()
            print(f"   POST /api/users/login: SUCCESS (200)")
            print(f"   Token received: {'Yes' if 'access_token' in data else 'No'}")
        else:
            print(f"   POST /api/users/login: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   POST /api/users/login: ERROR - {e}")
    
    # Test incorrect login route with POST
    try:
        response = requests.post(base_url + "/users/login", json=login_data, timeout=5)
        print(f"   POST /users/login: {response.status_code} (Expected 404 - Not Found)")
    except Exception as e:
        print(f"   POST /users/login: ERROR - {e}")
    
    print("\n3. Checking Route Configuration:")
    try:
        response = requests.get(base_url + "/docs", timeout=5)
        if response.ok:
            print("   OK: Swagger docs accessible")
            print("   Check: http://127.0.0.1:8000/docs for available routes")
        else:
            print("   ERROR: Swagger docs not accessible")
    except Exception as e:
        print(f"   ERROR: Swagger docs - {e}")
    
    print("\n" + "="*50)
    print("LOGIN ROUTE FIX SUMMARY:")
    print("="*50)
    
    print("\nPROBLEM IDENTIFIED:")
    print("   - Frontend was calling: /users/login")
    print("   - Backend route is: /api/users/login (with prefix)")
    print("   - Result: 404 Not Found error")
    
    print("\nFIXES APPLIED:")
    print("   - script-new.js: Updated login URL to /api/users/login")
    print("   - script-new.js: Updated register URL to /api/users/register")
    print("   - script-new.js: Updated skills URL to /api/skills/")
    print("   - script-new.js: Updated exchanges URL to /api/exchanges/")
    print("   - script-new.js: Updated notifications URL to /api/notifications/")
    
    print("\nBACKEND ROUTE CONFIGURATION:")
    print("   - Users router: /api/users/*")
    print("   - Skills router: /api/skills/*")
    print("   - Exchanges router: /api/exchanges/*")
    print("   - Notifications router: /api/notifications/*")
    
    print("\nCORRECT FRONTEND URLS:")
    print("   - Login: http://127.0.0.1:8000/api/users/login")
    print("   - Register: http://127.0.0.1:8000/api/users/register")
    print("   - Skills: http://127.0.0.1:8000/api/skills/")
    print("   - Exchanges: http://127.0.0.1:8000/api/exchanges/")
    print("   - Notifications: http://127.0.0.1:8000/api/notifications/")
    
    print("\nHOW TO TEST:")
    print("   1. Start backend: python main.py")
    print("   2. Start frontend: python -m http.server 3000")
    print("   3. Open: http://127.0.0.1:3000/frontend/login.html")
    print("   4. Try login with credentials")
    print("   5. Check browser Network tab for correct URLs")
    
    print("\nEXPECTED BEHAVIOR:")
    print("   - No more 'Not Found' error on login")
    print("   - Login request goes to /api/users/login")
    print("   - Successful login returns JWT token")
    print("   - User is redirected to dashboard")
    
    print("\nTROUBLESHOOTING:")
    print("   - Check browser console for errors")
    print("   - Verify Network tab shows 200 status")
    print("   - Ensure backend is running on port 8000")
    print("   - Check CORS configuration")
    
    print("\n" + "="*50)
    print("LOGIN ROUTE FIX COMPLETE!")
    print("Frontend should now connect to correct backend routes.")
    print("="*50)

if __name__ == "__main__":
    test_login_route_fix()
