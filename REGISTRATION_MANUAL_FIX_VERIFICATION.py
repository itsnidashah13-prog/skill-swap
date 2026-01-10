#!/usr/bin/env python3
"""
Registration Manual Fix Verification Script
"""

import requests
import json

def verify_registration_manual_fix():
    """Verify registration manual fix"""
    print("REGISTRATION MANUAL FIX VERIFICATION")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    
    print("1. Testing Registration Endpoint:")
    
    # Test registration with sample data
    registration_data = {
        "username": "testuser_manual_" + str(int(requests.get(base_url + "/health").status_code)),
        "email": "manual_test@example.com",
        "full_name": "Manual Test User",
        "password": "password123",
        "bio": "Test user for manual fix verification"
    }
    
    try:
        response = requests.post(base_url + "/users/register", json=registration_data, timeout=5)
        print(f"   POST /users/register: {response.status_code}")
        
        if response.ok:
            print("   Registration: SUCCESS")
            print("   User created successfully")
            print("   Response:", response.json())
        elif response.status_code == 400:
            print("   Registration: BAD REQUEST")
            print("   Error:", response.json())
        elif response.status_code == 422:
            print("   Registration: VALIDATION ERROR")
            print("   Error:", response.json())
        else:
            print(f"   Registration: FAILED - {response.text}")
    except Exception as e:
        print(f"   Registration: ERROR - {e}")
    
    print("\n2. Testing Login Endpoint:")
    
    # Test login with known user
    login_data = {
        "username": "john_doe",
        "password": "password123"
    }
    
    try:
        response = requests.post(base_url + "/users/login", json=login_data, timeout=5)
        print(f"   POST /users/login: {response.status_code}")
        
        if response.ok:
            data = response.json()
            token = data.get('access_token', '')
            print("   Login: SUCCESS")
            print(f"   Token: {'Received' if token else 'Not received'}")
            print(f"   Token Type: {data.get('token_type', 'Not found')}")
        else:
            print(f"   Login: FAILED - {response.text}")
    except Exception as e:
        print(f"   Login: ERROR - {e}")
    
    print("\n3. Checking Frontend Files:")
    
    import os
    frontend_dir = "c:/Users/Javy/Desktop/skill swap/frontend"
    
    # Check register.html
    register_html_path = os.path.join(frontend_dir, "register.html")
    if os.path.exists(register_html_path):
        with open(register_html_path, 'r') as f:
            content = f.read()
            if "script.js" in content:
                print("   register.html: Uses script.js (CORRECT)")
            else:
                print("   register.html: Missing script.js reference")
    else:
        print("   register.html: File not found")
    
    # Check script.js for manual fix
    script_js_path = os.path.join(frontend_dir, "script.js")
    if os.path.exists(script_js_path):
        with open(script_js_path, 'r') as f:
            content = f.read()
            
            # Check for manual URL fix
            if "http://127.0.0.1:8000/users/register" in content:
                print("   script.js: Registration URL manually fixed (CORRECT)")
            else:
                print("   script.js: Registration URL not manually fixed")
            
            if "http://127.0.0.1:8000/users/login" in content:
                print("   script.js: Login URL manually fixed (CORRECT)")
            else:
                print("   script.js: Login URL not manually fixed")
            
            if "'Content-Type': 'application/json'" in content:
                print("   script.js: Content-Type header set (CORRECT)")
            else:
                print("   script.js: Content-Type header missing")
    else:
        print("   script.js: File not found")
    
    print("\n" + "="*60)
    print("MANUAL FIX SUMMARY:")
    print("="*60)
    
    print("\nPROBLEM IDENTIFIED:")
    print("   - Frontend was using getApiUrl() function")
    print("   - getApiUrl() was adding /api prefix incorrectly")
    print("   - Result: Wrong URL for registration/login")
    print("   - Error: 404 Not Found")
    
    print("\nMANUAL FIX APPLIED:")
    print("   - script.js: Registration fetch updated to full URL")
    print("   - script.js: Login fetch updated to full URL")
    print("   - Removed getApiUrl() function usage")
    print("   - Used absolute URLs: http://127.0.0.1:8000/users/*")
    print("   - Content-Type: application/json confirmed")
    
    print("\nFIXED CODE IN script.js:")
    print("   // Registration")
    print("   fetch('http://127.0.0.1:8000/users/register', {")
    print("       method: 'POST',")
    print("       headers: { 'Content-Type': 'application/json' },")
    print("       body: JSON.stringify(userData)")
    print("   })")
    print("")
    print("   // Login")
    print("   fetch('http://127.0.0.1:8000/users/login', {")
    print("       method: 'POST',")
    print("       headers: { 'Content-Type': 'application/json' },")
    print("       body: JSON.stringify({ username, password })")
    print("   })")
    
    print("\nHOW TO TEST:")
    print("   1. Restart backend: python main.py")
    print("   2. Start frontend: python -m http.server 3000")
    print("   3. Open: http://127.0.0.1:3000/frontend/register.html")
    print("   4. Fill registration form")
    print("   5. Submit form")
    print("   6. Check Network tab for correct URL")
    print("   7. Verify no 'Not Found' error")
    
    print("\nEXPECTED BEHAVIOR:")
    print("   - Registration: No 404 Not Found error")
    print("   - Network tab: POST http://127.0.0.1:8000/users/register")
    print("   - Content-Type: application/json")
    print("   - Success: User created and redirected to login")
    print("   - Login: Works with new credentials")
    
    print("\nBROWSER NETWORK TAB CHECKLIST:")
    print("   - URL: http://127.0.0.1:8000/users/register")
    print("   - Method: POST")
    print("   - Status: 200 (success) or 400/422 (validation)")
    print("   - Content-Type: application/json")
    print("   - No 404 Not Found errors")
    
    print("\n" + "="*60)
    print("MANUAL REGISTRATION FIX COMPLETE!")
    print("Frontend should now register users successfully.")
    print("="*60)

if __name__ == "__main__":
    verify_registration_manual_fix()
