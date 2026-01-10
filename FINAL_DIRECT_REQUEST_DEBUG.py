#!/usr/bin/env python3
"""
Final Direct Request Debug Script
"""

import requests
import json

def final_direct_request_debug():
    """Final debug for direct_request_skill function"""
    print("FINAL DIRECT REQUEST DEBUG")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    
    print("1. TESTING DIRECT_REQUEST_SKILL WITH DETAILED LOGGING:")
    print("-" * 50)
    
    # First login to get token
    login_data = {
        "username": "john_doe",
        "password": "password123"
    }
    
    try:
        print("   Step 1: Logging in...")
        login_response = requests.post(base_url + "/users/login", json=login_data, timeout=10)
        
        if login_response.ok:
            token_data = login_response.json()
            token = token_data.get('access_token', '')
            print(f"   Login: SUCCESS (Token: {'Received' if token else 'Not received'})")
            
            if token:
                # Get available skills
                print("   Step 2: Getting available skills...")
                headers = {"Authorization": f"Bearer {token}"}
                skills_response = requests.get(base_url + "/api/skills/", headers=headers, timeout=10)
                
                if skills_response.ok:
                    skills = skills_response.json()
                    print(f"   Skills: SUCCESS (Found {len(skills)} skills)")
                    
                    if skills:
                        # Try to create exchange request for first skill
                        skill_id = skills[0]['id']
                        skill_title = skills[0]['title']
                        print(f"   Step 3: Testing direct_request_skill for skill ID {skill_id} ({skill_title})...")
                        
                        exchange_data = {
                            "skill_id": skill_id,
                            "message": "Final debug test - detailed logging enabled"
                        }
                        
                        print("   Step 4: Sending request to /request-skill endpoint...")
                        print(f"   Request URL: {base_url}/request-skill")
                        print(f"   Request data: {json.dumps(exchange_data, indent=2)}")
                        print(f"   Authorization: Bearer {token[:30]}...")
                        
                        print("\n   Step 5: WATCH YOUR BACKEND TERMINAL FOR DEBUG OUTPUT!")
                        print("   You should see these messages:")
                        print("     - DEBUG: Creating skill exchange request with data:")
                        print("     - DEBUG: Adding request to database...")
                        print("     - DEBUG: Committing to database...")
                        print("     - DEBUG: Refreshing request object...")
                        print("     - DEBUG: Skill exchange request created successfully with ID: [number]")
                        print("     - DEBUG: Creating notification for skill owner...")
                        print("     - DEBUG: Skill owner ID: [number]")
                        print("     - DEBUG: Skill owner username: [username]")
                        print("     - DEBUG: Requester: [username]")
                        print("     - DEBUG: Skill title: [title]")
                        print("     - DEBUG: Calling create_notification...")
                        print("     - DEBUG: Notification created successfully")
                        print("     - DEBUG: Preparing response...")
                        print("     - DEBUG: Skill owner username: [username]")
                        
                        print("\n   Step 6: Sending request now...")
                        
                        direct_response = requests.post(
                            base_url + "/request-skill", 
                            json=exchange_data, 
                            headers=headers, 
                            timeout=10
                        )
                        
                        print(f"   Step 7: Response received")
                        print(f"   Status Code: {direct_response.status_code}")
                        print(f"   Response Headers: {dict(direct_response.headers)}")
                        
                        if direct_response.ok:
                            result = direct_response.json()
                            print("   Direct Request: SUCCESS")
                            print(f"   Success: {result.get('success', 'Not found')}")
                            print(f"   Message: {result.get('message', 'Not found')}")
                            print(f"   Request ID: {result.get('request_id', 'Not found')}")
                            print(f"   Skill Title: {result.get('skill_title', 'Not found')}")
                            print(f"   Skill Owner: {result.get('skill_owner', 'Not found')}")
                            
                            print("\n   SUCCESS! The direct_request_skill function is working correctly!")
                            print("   All debug messages should have appeared in your terminal.")
                            
                        else:
                            print("   Direct Request: FAILED")
                            print(f"   Status Code: {direct_response.status_code}")
                            print(f"   Response Text: {direct_response.text}")
                            
                            # Try to parse error response
                            try:
                                error_json = direct_response.json()
                                print(f"   Error JSON: {json.dumps(error_json, indent=2)}")
                            except:
                                print("   Error Response: Not valid JSON")
                            
                            print("\n   CHECK YOUR TERMINAL FOR ERROR MESSAGES:")
                            print("     - ERROR: Failed to create skill exchange request: [error]")
                            print("     - ERROR: Exception type: [type]")
                            print("     - ERROR: Exception details: [details]")
                            print("     - ERROR: Notification creation failed: [error]")
                            print("     - Error in direct_request_skill: [error]")
                        
                    else:
                        print("   Direct Request: SKIPPED - No skills available")
                else:
                    print(f"   Skills: FAILED - {skills_response.text}")
            else:
                print("   Direct Request: SKIPPED - No token received")
        else:
            print(f"   Login: FAILED - {login_response.text}")
    except Exception as e:
        print(f"   Debug Flow: ERROR - {e}")
        print(f"   Exception Type: {type(e).__name__}")
        print(f"   Exception Details: {str(e)}")
    
    print("\n" + "="*60)
    print("DEBUGGING INSTRUCTIONS:")
    print("="*60)
    
    print("\nBACKEND DEBUGGING:")
    print("   1. Restart backend: python main.py")
    print("   2. Watch terminal for ALL debug messages")
    print("   3. Run this script again")
    print("   4. Look for specific debug output listed above")
    
    print("\nEXPECTED DEBUG OUTPUT (IF WORKING):")
    print("   - All DEBUG messages should appear")
    print("   - No ERROR messages")
    print("   - Response should be 200 OK")
    print("   - Skill owner username should be displayed")
    
    print("\nEXPECTED ERROR OUTPUT (IF NOT WORKING):")
    print("   - ERROR messages with specific details")
    print("   - Exception type and details")
    print("   - Clear indication of what's failing")
    
    print("\nCOMMON ISSUES TO CHECK:")
    print("   - Database connection issues")
    print("   - Missing skill in database")
    print("   - User not found")
    print("   - Notification creation failure")
    print("   - Skill user relationship issues")
    
    print("\n" + "="*60)
    print("FINAL DEBUG SCRIPT COMPLETE!")
    print("Run this script and watch your backend terminal for detailed output.")
    print("="*60)

if __name__ == "__main__":
    final_direct_request_debug()
