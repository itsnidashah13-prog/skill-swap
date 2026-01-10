#!/usr/bin/env python3
"""
Local Server Fix - Test your local Skill Swap application
"""

import requests
import json
import time

def test_local_server():
    """Test if local server is working"""
    print("TESTING LOCAL SKILL SWAP SERVER")
    print("="*50)
    
    # Test local server endpoints
    local_urls = [
        ("Root", "http://127.0.0.1:8000/"),
        ("Health", "http://127.0.0.1:8000/health"),
        ("Admin", "http://127.0.0.1:8000/admin/"),
        ("API Users", "http://127.0.0.1:8000/api/users/"),
        ("API Skills", "http://127.0.0.1:8000/api/skills/"),
        ("Frontend", "http://127.0.0.1:3002/frontend/index.html")
    ]
    
    all_working = True
    
    for name, url in local_urls:
        print(f"\nTesting {name}: {url}")
        
        try:
            # Set timeout to 5 seconds
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {name} - Working (Status: {response.status_code})")
                
                # Check if it's JSON or HTML
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    print(f"   Type: JSON API")
                elif 'text/html' in content_type:
                    print(f"   Type: HTML Page")
                else:
                    print(f"   Type: {content_type}")
                    
            elif response.status_code == 404:
                print(f"❌ {name} - Not Found (404)")
                all_working = False
            else:
                print(f"⚠️  {name} - Status: {response.status_code}")
                if response.status_code >= 500:
                    all_working = False
                    
        except requests.exceptions.ConnectionError:
            print(f"❌ {name} - Connection Refused")
            print(f"   Server not running on this port")
            all_working = False
        except requests.exceptions.Timeout:
            print(f"⏰ {name} - Request Timeout")
            all_working = False
        except Exception as e:
            print(f"❌ {name} - Error: {e}")
            all_working = False
    
    print(f"\n{'='*50}")
    print("SUMMARY:")
    
    if all_working:
        print("✅ All local endpoints are working!")
        print("\nNEXT STEPS:")
        print("1. Your local server is running correctly")
        print("2. Open browser to: http://127.0.0.1:3002/frontend/index.html")
        print("3. Test login and skill exchange features")
        print("4. Ignore external API timeout errors")
    else:
        print("❌ Some local endpoints are not working!")
        print("\nTROUBLESHOOTING:")
        print("1. Start your local server:")
        print("   cd 'c:/Users/Javy/Desktop/skill swap'")
        print("   python main.py")
        print("2. Wait for 'Uvicorn running on http://127.0.0.1:8000'")
        print("3. Check if port 8000 is available")
        print("4. Try alternative: http://localhost:8000/")
    
    print(f"\n{'='*50}")
    print("EXTERNAL API ERROR EXPLANATION:")
    print("The timeout error you're seeing is from:")
    print("- server.self-serve.windsurf.com (External API)")
    print("- NOT your local Skill Swap application")
    print("\nThis error is unrelated to your project.")
    print("Your local app should work fine once server is running.")
    
    return all_working

def start_local_server():
    """Start local server with proper settings"""
    print("\nSTARTING LOCAL SKILL SWAP SERVER")
    print("="*50)
    
    import subprocess
    import sys
    
    try:
        # Start the server
        print("Starting FastAPI server...")
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd="c:/Users/Javy/Desktop/skill swap")
        
        print("✅ Server started!")
        print("Waiting 3 seconds for server to initialize...")
        time.sleep(3)
        
        # Test if server is responding
        if test_local_server():
            print("\n🎉 SERVER IS READY!")
            print("\nOpen these URLs:")
            print("- Frontend: http://127.0.0.1:3002/frontend/index.html")
            print("- Admin: http://127.0.0.1:8000/admin/")
            print("- API Docs: http://127.0.0.1:8000/docs")
            print("\nPress Ctrl+C to stop the server")
            
            # Keep script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 Server stopped by user")
                process.terminate()
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 LOCAL SKILL SWAP SERVER FIX")
    print("="*50)
    print("This script tests and starts your local Skill Swap server.")
    print("It ignores external API errors and focuses on your local application.")
    print("="*50)
    
    # First test current server status
    print("\n1. Testing current server status...")
    if test_local_server():
        print("\n2. Server is already running correctly!")
        print("\n✅ Your Skill Swap application is working!")
        print("✅ The external API timeout error is unrelated.")
        print("\nOpen: http://127.0.0.1:3002/frontend/index.html")
    else:
        print("\n2. Starting local server...")
        start_local_server()
