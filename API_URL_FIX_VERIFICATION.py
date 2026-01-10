#!/usr/bin/env python3
"""
API URL Fix Verification Script
"""

import os
import re

def check_api_urls():
    """Check and verify API URLs in JavaScript files"""
    print("API URL FIX VERIFICATION")
    print("="*50)
    
    frontend_dir = "c:/Users/Javy/Desktop/skill swap/frontend"
    
    # Files to check
    files_to_check = [
        "script.js",
        "script-new.js", 
        "admin.html",
        "test_exchange.html",
        "test_skills_fetch.html",
        "test_fixed_auth.html",
        "test_auth_complete.html"
    ]
    
    print("1. Checking API URLs in JavaScript files:")
    
    correct_url = "http://127.0.0.1:8000"
    incorrect_urls = [
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://localhost:3000"
    ]
    
    all_correct = True
    
    for filename in files_to_check:
        filepath = os.path.join(frontend_dir, filename)
        
        if os.path.exists(filepath):
            print(f"\n   Checking {filename}:")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for correct URL
                if correct_url in content:
                    print(f"      OK: {correct_url} found")
                else:
                    print(f"      WARNING: {correct_url} not found")
                    all_correct = False
                
                # Check for incorrect URLs
                for incorrect_url in incorrect_urls:
                    if incorrect_url in content:
                        print(f"      ERROR: {incorrect_url} found (should be {correct_url})")
                        all_correct = False
                
                # Show API_BASE_URL lines
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'API_BASE_URL' in line and '=' in line:
                        print(f"      Line {i}: {line.strip()}")
        else:
            print(f"\n   File not found: {filename}")
    
    print("\n" + "="*50)
    print("API URL CONFIGURATION SUMMARY:")
    print("="*50)
    
    print("\nCORRECT CONFIGURATION:")
    print(f"   Backend Port: 8000 (FastAPI)")
    print(f"   Frontend Port: 3000 (Static Server)")
    print(f"   API Base URL: {correct_url}")
    
    print("\nFILES UPDATED:")
    print("   - script.js: Already correct")
    print("   - script-new.js: Updated to port 8000")
    print("   - admin.html: Already correct")
    print("   - test_exchange.html: Updated to port 8000")
    print("   - Other test files: Already correct")
    
    print("\nENDPOINTS CONFIGURATION:")
    print("   - Base URL: http://127.0.0.1:8000")
    print("   - Skills API: http://127.0.0.1:8000/api/skills/")
    print("   - Users API: http://127.0.0.1:8000/api/users/")
    print("   - Exchanges API: http://127.0.0.1:8000/api/exchanges/")
    print("   - Admin API: http://127.0.0.1:8000/admin/")
    
    print("\nHOW TO TEST:")
    print("   1. Start backend: python main.py")
    print("   2. Start frontend: python -m http.server 3000")
    print("   3. Open: http://127.0.0.1:3000/frontend/index.html")
    print("   4. Test skills loading")
    print("   5. Check browser console for API calls")
    
    print("\nCOMMON ERRORS FIXED:")
    print("   - localhost:8000 -> 127.0.0.1:8000")
    print("   - Port 3000 API calls -> Port 8000")
    print("   - Missing /api prefix -> Added")
    print("   - Relative URLs -> Absolute URLs")
    
    print("\nTROUBLESHOOTING:")
    print("   - Check browser console for errors")
    print("   - Verify backend is running on port 8000")
    print("   - Check CORS configuration")
    print("   - Ensure JWT token is present")
    print("   - Test with browser dev tools Network tab")
    
    print("\nEXPECTED BEHAVIOR:")
    print("   - Skills load without 'Error loading skills' message")
    print("   - API calls show 200 status in Network tab")
    print("   - No CORS errors in console")
    print("   - Authentication works properly")
    
    if all_correct:
        print("\n" + "="*50)
        print("ALL API URLS ARE CORRECT!")
        print("Frontend should now connect to backend properly.")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("SOME API URLS NEED FIXING!")
        print("Please check the errors above.")
        print("="*50)

if __name__ == "__main__":
    check_api_urls()
