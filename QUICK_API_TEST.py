#!/usr/bin/env python3
"""
Quick API Test to verify backend connectivity
"""

import requests
import json

def quick_api_test():
    """Quick test of backend API endpoints"""
    print("QUICK API TEST - Backend Connectivity")
    print("="*50)
    
    base_url = "http://127.0.0.1:8000"
    
    print("1. Testing Backend Server:")
    try:
        response = requests.get(base_url + "/", timeout=5)
        if response.ok:
            print("   OK: Backend is running on port 8000")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ERROR: Backend returned {response.status_code}")
            return
    except Exception as e:
        print(f"   ERROR: Backend not accessible - {e}")
        print("   Make sure backend is running: python main.py")
        return
    
    print("\n2. Testing Skills API:")
    try:
        response = requests.get(base_url + "/api/skills/", timeout=5)
        if response.ok:
            skills = response.json()
            print(f"   OK: Skills API working - Found {len(skills)} skills")
            if skills:
                print(f"   Sample: {skills[0].get('title', 'Unknown')}")
        else:
            print(f"   ERROR: Skills API returned {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Skills API failed - {e}")
    
    print("\n3. Testing Health Endpoint:")
    try:
        response = requests.get(base_url + "/health", timeout=5)
        if response.ok:
            print("   OK: Health endpoint working")
        else:
            print(f"   ERROR: Health endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Health endpoint failed - {e}")
    
    print("\n4. Testing Admin Endpoints:")
    try:
        response = requests.get(base_url + "/admin/users-json", timeout=5)
        if response.ok:
            data = response.json()
            print(f"   OK: Admin users endpoint - {data.get('count', 0)} users")
        else:
            print(f"   ERROR: Admin users endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Admin users endpoint failed - {e}")
    
    print("\n" + "="*50)
    print("FRONTEND TESTING INSTRUCTIONS:")
    print("="*50)
    
    print("\n1. Start Frontend Server:")
    print("   cd frontend")
    print("   python -m http.server 3000")
    
    print("\n2. Open Frontend:")
    print("   http://127.0.0.1:3000/frontend/index.html")
    
    print("\n3. Test Skills Loading:")
    print("   - Check if skills load without error")
    print("   - Look for 'Error loading skills' message")
    print("   - Check browser console for API calls")
    
    print("\n4. Check Browser Network Tab:")
    print("   - Open Developer Tools (F12)")
    print("   - Go to Network tab")
    print("   - Look for API calls to 127.0.0.1:8000")
    print("   - Check for 200 status codes")
    
    print("\n5. Common Issues:")
    print("   - CORS errors: Check backend CORS settings")
    print("   - 404 errors: Wrong endpoint URL")
    print("   - 401 errors: Authentication required")
    print("   - Network errors: Backend not running")
    
    print("\n6. Expected URLs in Network Tab:")
    print("   GET http://127.0.0.1:8000/api/skills/")
    print("   GET http://127.0.0.1:8000/api/users/me")
    print("   POST http://127.0.0.1:8000/request-skill")
    
    print("\n" + "="*50)
    print("API URL FIX SUMMARY:")
    print("="*50)
    
    print("\nFIXED FILES:")
    print("   - script-new.js: Updated to 127.0.0.1:8000")
    print("   - test_exchange.html: Updated to 127.0.0.1:8000")
    print("   - All other files: Already correct")
    
    print("\nCORRECT CONFIGURATION:")
    print("   Backend: http://127.0.0.1:8000 (FastAPI)")
    print("   Frontend: http://127.0.0.1:3000 (Static Server)")
    print("   API Base: http://127.0.0.1:8000")
    
    print("\nNEXT STEPS:")
    print("   1. Start both servers")
    print("   2. Open frontend in browser")
    print("   3. Test skills loading")
    print("   4. Check for error messages")
    
    print("="*50)

if __name__ == "__main__":
    quick_api_test()
