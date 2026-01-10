#!/usr/bin/env python3
"""
Debug server errors and fix them
"""

import requests
import json

def debug_endpoints():
    """Debug specific endpoints that are failing"""
    print("DEBUGGING SERVER ERRORS")
    print("="*50)
    
    # Test Admin endpoint
    print("\n1. Testing Admin endpoint...")
    try:
        response = requests.get("http://127.0.0.1:8000/admin/", timeout=5)
        print(f"Admin Status: {response.status_code}")
        if response.status_code == 500:
            print("Admin endpoint has server error")
            print("Possible cause: SQLAdmin router not properly imported")
    except Exception as e:
        print(f"Admin Error: {e}")
    
    # Test Users API endpoint
    print("\n2. Testing Users API endpoint...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/users/", timeout=5)
        print(f"Users API Status: {response.status_code}")
        if response.status_code == 500:
            print("Users API has server error")
            print("Possible cause: CRUD function error or database issue")
            
            # Try to get error details
            try:
                error_response = response.text
                print(f"Error details: {error_response[:200]}...")
            except:
                pass
    except Exception as e:
        print(f"Users API Error: {e}")
    
    # Test working endpoints
    print("\n3. Testing working endpoints...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/skills/", timeout=5)
        print(f"Skills API Status: {response.status_code}")
        if response.status_code == 200:
            print("Skills API is working correctly")
    except Exception as e:
        print(f"Skills API Error: {e}")

def check_imports():
    """Check if all imports are working"""
    print("\n4. Checking imports...")
    
    try:
        import main
        print("SUCCESS: main.py imports correctly")
    except Exception as e:
        print(f"ERROR: main.py import failed: {e}")
    
    try:
        from sql_admin import sql_admin_router
        print("SUCCESS: sql_admin imports correctly")
    except Exception as e:
        print(f"ERROR: sql_admin import failed: {e}")
    
    try:
        from crud import create_user, update_user
        print("SUCCESS: CRUD functions import correctly")
    except Exception as e:
        print(f"ERROR: CRUD import failed: {e}")

def suggest_fixes():
    """Suggest specific fixes"""
    print("\n" + "="*50)
    print("SUGGESTED FIXES:")
    print("="*50)
    
    print("\n1. FOR ADMIN ERROR (500):")
    print("   - Check if sql_admin.py exists")
    print("   - Verify sql_admin_router is imported in main.py")
    print("   - Check database connection in admin functions")
    
    print("\n2. FOR USERS API ERROR (500):")
    print("   - Check CRUD functions are fixed (.dict() -> .model_dump())")
    print("   - Verify database tables exist")
    print("   - Check user model imports")
    
    print("\n3. QUICK FIXES:")
    print("   a) Restart server: python main.py")
    print("   b) Check server console for error messages")
    print("   c) Test individual functions")
    
    print("\n4. EXTERNAL API ERROR:")
    print("   - The timeout error is from server.self-serve.windsurf.com")
    print("   - This is NOT your local application")
    print("   - Your local app works independently")

if __name__ == "__main__":
    debug_endpoints()
    check_imports()
    suggest_fixes()
