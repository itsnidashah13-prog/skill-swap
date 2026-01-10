#!/usr/bin/env python3
"""
Complete Skill Exchange Debug Script
"""

import requests
import json

def complete_skill_exchange_debug():
    """Complete debug for skill exchange request"""
    print("COMPLETE SKILL EXCHANGE DEBUG")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    
    print("1. TESTING SKILL EXCHANGE REQUEST WITH DETAILED DEBUGGING:")
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
                        print(f"   Step 3: Testing skill exchange request for skill ID {skill_id} ({skill_title})...")
                        
                        exchange_data = {
                            "skill_id": skill_id,
                            "message": "Complete debug test - university project"
                        }
                        
                        print("   Step 4: Sending request to /request-skill endpoint...")
                        print(f"   Request URL: {base_url}/request-skill")
                        print(f"   Request data: {json.dumps(exchange_data, indent=2)}")
                        print(f"   Authorization: Bearer {token[:30]}...")
                        
                        print("\n   Step 5: WATCH YOUR BACKEND TERMINAL FOR DEBUG OUTPUT!")
                        print("   You should see these messages:")
                        print("     - DEBUG: Received skill exchange request")
                        print("     - DEBUG: Authorization header: Bearer <token>")
                        print("     - DEBUG: Extracted token: <token>...")
                        print("     - DEBUG: Decoded username: <username>")
                        print("     - DEBUG: Found user: <username> (ID: <id>)")
                        print("     - DEBUG: Request data - skill_id: <id>, message: '<message>'")
                        print("     - DEBUG: Found skill: <title> (ID: <id>, Owner: <id>)")
                        print("     - DEBUG: Creating exchange request...")
                        print("     - DEBUG: Exchange request created with ID: <id>")
                        print("     - DEBUG: Creating notification for skill owner...")
                        print("     - DEBUG: Notification created successfully")
                        print("     - DEBUG: Preparing response...")
                        print("     - DEBUG: Skill owner username: <username>")
                        
                        print("\n   Step 6: Sending request now...")
                        
                        exchange_response = requests.post(
                            base_url + "/request-skill", 
                            json=exchange_data, 
                            headers=headers, 
                            timeout=10
                        )
                        
                        print(f"   Step 7: Response received")
                        print(f"   Status Code: {exchange_response.status_code}")
                        print(f"   Response Headers: {dict(exchange_response.headers)}")
                        
                        if exchange_response.ok:
                            result = exchange_response.json()
                            print("   Exchange Request: SUCCESS")
                            print(f"   Success: {result.get('success', 'Not found')}")
                            print(f"   Message: {result.get('message', 'Not found')}")
                            print(f"   Request ID: {result.get('request_id', 'Not found')}")
                            print(f"   Skill Title: {result.get('skill_title', 'Not found')}")
                            print(f"   Skill Owner: {result.get('skill_owner', 'Not found')}")
                            
                            print("\n   ✅ SUCCESS! The skill exchange request is working correctly!")
                            print("   All debug messages should have appeared in your terminal.")
                            
                        else:
                            print("   Exchange Request: FAILED")
                            print(f"   Status Code: {exchange_response.status_code}")
                            print(f"   Response Text: {exchange_response.text}")
                            
                            # Try to parse error response
                            try:
                                error_json = exchange_response.json()
                                print(f"   Error JSON: {json.dumps(error_json, indent=2)}")
                            except:
                                print("   Error Response: Not valid JSON")
                            
                            print("\n   CHECK YOUR TERMINAL FOR ERROR MESSAGES:")
                            print("     - ERROR: Invalid authorization header")
                            print("     - ERROR: Invalid token")
                            print("     - ERROR: Token has expired")
                            print("     - ERROR: User not found in database")
                            print("     - ERROR: Empty message")
                            print("     - ERROR: Invalid skill_id")
                            print("     - ERROR: Skill not found")
                            print("     - ERROR: User requesting own skill")
                            print("     - ERROR: Notification creation failed")
                            print("     - ERROR: Unexpected error in direct_request_skill")
                        
                    else:
                        print("   Exchange Request: SKIPPED - No skills available")
                else:
                    print(f"   Skills: FAILED - {skills_response.text}")
            else:
                print("   Exchange Request: SKIPPED - No token received")
        else:
            print(f"   Login: FAILED - {login_response.text}")
    except Exception as e:
        print(f"   Debug Flow: ERROR - {e}")
        print(f"   Exception Type: {type(e).__name__}")
        print(f"   Exception Details: {str(e)}")
    
    print("\n" + "="*60)
    print("COMPLETE DEBUGGING INSTRUCTIONS:")
    print("="*60)
    
    print("\nBACKEND DEBUGGING:")
    print("   1. Restart backend: python main.py")
    print("   2. Watch terminal for ALL debug messages")
    print("   3. Run this script again")
    print("   4. Look for specific debug messages listed above")
    
    print("\nFRONTEND DEBUGGING:")
    print("   1. Open browser Developer Tools (F12)")
    print("   2. Go to Console tab")
    print("   3. Try to create exchange request")
    print("   4. Check for JavaScript errors")
    print("   5. Check Network tab for request details")
    
    print("\nCOMMON ISSUES TO CHECK:")
    print("   - Invalid or expired JWT token")
    print("   - User not found in database")
    print("   - Skill not found in database")
    print("   - User requesting their own skill")
    print("   - Database connection issues")
    print("   - Foreign key constraint violations")
    print("   - Notification creation failures")
    
    print("\nEXPECTED DEBUG OUTPUT (IF WORKING):")
    print("   - DEBUG: Received skill exchange request")
    print("   - DEBUG: Authorization header: Bearer <token>")
    print("   - DEBUG: Extracted token: <token>...")
    print("   - DEBUG: Decoded username: <username>")
    print("   - DEBUG: Found user: <username> (ID: <id>)")
    print("   - DEBUG: Request data - skill_id: <id>, message: '<message>'")
    print("   - DEBUG: Found skill: <title> (ID: <id>, Owner: <id>)")
    print("   - DEBUG: Creating exchange request...")
    print("   - DEBUG: Exchange request created with ID: <id>")
    print("   - DEBUG: Creating notification for skill owner...")
    print("   - DEBUG: Notification created successfully")
    print("   - DEBUG: Preparing response...")
    print("   - DEBUG: Skill owner username: <username>")
    
    print("\nEXPECTED DEBUG OUTPUT (IF ERROR):")
    print("   - ERROR: Invalid authorization header")
    print("   - ERROR: Invalid token")
    print("   - ERROR: Token has expired")
    print("   - ERROR: User not found in database")
    print("   - ERROR: Skill not found")
    print("   - ERROR: User requesting own skill")
    print("   - ERROR: Notification creation failed")
    print("   - ERROR: Unexpected error in direct_request_skill")
    
    print("\n" + "="*60)
    print("COMPLETE DEBUG SCRIPT READY!")
    print("Run this script and watch your backend terminal for detailed error messages.")
    print("="*60)

if __name__ == "__main__":
    complete_skill_exchange_debug()
