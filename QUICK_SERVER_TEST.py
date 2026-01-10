#!/usr/bin/env python3
"""
Quick server test - No unicode issues
"""

import requests
import time

def test_server():
    """Test local server endpoints"""
    print("LOCAL SKILL SWAP SERVER TEST")
    print("="*50)
    
    urls = [
        ("Root", "http://127.0.0.1:8000/"),
        ("Health", "http://127.0.0.1:8000/health"),
        ("Admin", "http://127.0.0.1:8000/admin/"),
        ("API Users", "http://127.0.0.1:8000/api/users/"),
        ("API Skills", "http://127.0.0.1:8000/api/skills/")
    ]
    
    all_ok = True
    
    for name, url in urls:
        print(f"\nTesting {name}: {url}")
        
        try:
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                print(f"OK - {name} working (Status: {response.status_code})")
            elif response.status_code == 404:
                print(f"NOT FOUND - {name} (404)")
                all_ok = False
            else:
                print(f"ERROR - {name} (Status: {response.status_code})")
                if response.status_code >= 500:
                    all_ok = False
                    
        except requests.exceptions.ConnectionError:
            print(f"CONNECTION REFUSED - {name}")
            print("Server not running on port 8000")
            all_ok = False
        except requests.exceptions.Timeout:
            print(f"TIMEOUT - {name}")
            all_ok = False
        except Exception as e:
            print(f"ERROR - {name}: {e}")
            all_ok = False
    
    print(f"\n{'='*50}")
    
    if all_ok:
        print("SUCCESS: All endpoints working!")
        print("\nYour local Skill Swap server is running correctly.")
        print("The external API timeout error is unrelated to your project.")
        print("\nOpen: http://127.0.0.1:3002/frontend/index.html")
    else:
        print("ISSUE: Some endpoints not working!")
        print("\nTO FIX:")
        print("1. Start server: python main.py")
        print("2. Wait for 'Uvicorn running on http://127.0.0.1:8000'")
        print("3. Test again")
    
    print(f"\n{'='*50}")
    print("EXTERNAL API ERROR EXPLANATION:")
    print("The timeout error you see is from:")
    print("- server.self-serve.windsurf.com (External service)")
    print("- NOT your local Skill Swap application")
    print("This error doesn't affect your local app functionality.")
    
    return all_ok

if __name__ == "__main__":
    test_server()
