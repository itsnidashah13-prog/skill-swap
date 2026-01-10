#!/usr/bin/env python3
"""
Test script to check admin interface access
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_admin_access():
    """Test all admin URLs"""
    
    print("🔍 TESTING ADMIN INTERFACE ACCESS")
    print("="*50)
    
    # Test URLs in order
    admin_urls = [
        ("/", "Admin Dashboard"),
        ("/login/", "Admin Login"),
        ("/auth/user/", "User Management"),
        ("/skills/skill/", "Skill Management"),
        ("/skills/skill/add/", "Add Skill Form"),
        ("/exchanges/skillexchangerequest/", "Request Management")
    ]
    
    for url, description in admin_urls:
        full_url = f"{BASE_URL}/admin{url}"
        print(f"\n📋 Testing: {description}")
        print(f"URL: {full_url}")
        
        try:
            response = requests.get(full_url, timeout=5)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS - Page loads correctly")
                
                # Check if it's HTML or JSON
                content_type = response.headers.get('content-type', '')
                if 'text/html' in content_type:
                    print("✅ HTML content - Admin interface working")
                elif 'application/json' in content_type:
                    print("📊 JSON content - API endpoint working")
                    
            elif response.status_code == 404:
                print("❌ NOT FOUND - URL not configured")
            elif response.status_code == 500:
                print("🔥 SERVER ERROR - Check server logs")
            else:
                print(f"⚠️  UNEXPECTED STATUS - {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR - Server not running")
        except requests.exceptions.Timeout:
            print("⏰ TIMEOUT - Server not responding")
        except Exception as e:
            print(f"❌ ERROR - {e}")
    
    print(f"\n{'='*50}")
    print("🚀 CORRECT URLS TO ACCESS:")
    print("="*50)
    
    correct_urls = [
        ("Admin Dashboard", "http://127.0.0.1:8000/admin/"),
        ("User Management", "http://127.0.0.1:8000/admin/auth/user/"),
        ("Skill Management", "http://127.0.0.1:8000/admin/skills/skill/"),
        ("Add Skill", "http://127.0.0.1:8000/admin/skills/skill/add/"),
        ("API Root", "http://127.0.0.1:8000/"),
        ("Health Check", "http://127.0.0.1:8000/health"),
    ]
    
    for name, url in correct_urls:
        print(f"{name:20} : {url}")
    
    print(f"\n{'='*50}")
    print("🛠️ TROUBLESHOOTING STEPS:")
    print("="*50)
    
    steps = [
        "1. Start the server: python main.py",
        "2. Wait for 'Uvicorn running on http://127.0.0.1:8000' message",
        "3. Open browser and try: http://127.0.0.1:8000/admin/",
        "4. If still not working, check if port 8000 is available",
        "5. Try alternative: http://localhost:8000/admin/",
        "6. Check if firewall is blocking the connection",
        "7. Verify all dependencies are installed: pip install jinja2 fastapi",
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n{'='*50}")
    print("📋 SERVER START COMMANDS:")
    print("="*50)
    
    print("Option 1 - Quick Start:")
    print("  START_DJANGO_ADMIN.bat")
    print()
    print("Option 2 - Manual Start:")
    print("  cd \"c:/Users/Javy/Desktop/skill swap\"")
    print("  python main.py")
    print()
    print("Option 3 - Check Dependencies:")
    print("  pip install jinja2 fastapi uvicorn")

if __name__ == "__main__":
    test_admin_access()
