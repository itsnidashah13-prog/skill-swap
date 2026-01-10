#!/usr/bin/env python3
"""
Capture Terminal Error Trace Script
"""

import subprocess
import time
import requests
import json
import threading
import sys

def capture_backend_output():
    """Capture backend output in real-time"""
    print("CAPTURING BACKEND TERMINAL OUTPUT")
    print("="*60)
    
    # Start backend process
    print("Starting backend process...")
    process = subprocess.Popen(
        ['python', 'main.py'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    def read_output():
        """Read output in real-time"""
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(f"BACKEND: {line.strip()}")
    
    # Start reading output in background
    output_thread = threading.Thread(target=read_output)
    output_thread.daemon = True
    output_thread.start()
    
    # Wait for backend to start
    time.sleep(3)
    
    try:
        print("\nTESTING SKILL EXCHANGE REQUEST TO TRIGGER ERROR...")
        print("-" * 50)
        
        # Test 1: Request without authorization
        print("Test 1: Request without authorization header")
        try:
            response = requests.post(
                'http://127.0.0.1:8000/request-skill', 
                json={'skill_id': 1, 'message': 'test'}, 
                timeout=5
            )
            print(f"Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Request error: {e}")
        
        time.sleep(1)
        
        # Test 2: Request with invalid token
        print("\nTest 2: Request with invalid token")
        try:
            headers = {'Authorization': 'Bearer invalid_token_here'}
            response = requests.post(
                'http://127.0.0.1:8000/request-skill', 
                json={'skill_id': 1, 'message': 'test'}, 
                headers=headers,
                timeout=5
            )
            print(f"Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Request error: {e}")
        
        time.sleep(1)
        
        # Test 3: Try to login first
        print("\nTest 3: Attempting login...")
        try:
            login_data = {'username': 'test_user', 'password': 'test_password'}
            login_response = requests.post(
                'http://127.0.0.1:8000/users/login', 
                json=login_data, 
                timeout=5
            )
            print(f"Login Response: {login_response.status_code} - {login_response.text}")
            
            if login_response.ok:
                token_data = login_response.json()
                token = token_data.get('access_token', '')
                
                if token:
                    print(f"Got token: {token[:30]}...")
                    
                    # Test 4: Valid token request
                    print("\nTest 4: Request with valid token")
                    headers = {'Authorization': f'Bearer {token}'}
                    
                    # Get skills first
                    skills_response = requests.get(
                        'http://127.0.0.1:8000/api/skills/', 
                        headers=headers,
                        timeout=5
                    )
                    print(f"Skills Response: {skills_response.status_code}")
                    
                    if skills_response.ok:
                        skills = skills_response.json()
                        if skills:
                            skill_id = skills[0]['id']
                            print(f"Using skill ID: {skill_id}")
                            
                            # Make exchange request
                            exchange_data = {
                                'skill_id': skill_id,
                                'message': 'Test request to capture error'
                            }
                            
                            exchange_response = requests.post(
                                'http://127.0.0.1:8000/request-skill', 
                                json=exchange_data, 
                                headers=headers,
                                timeout=5
                            )
                            print(f"Exchange Response: {exchange_response.status_code} - {exchange_response.text}")
                        else:
                            print("No skills available")
                    else:
                        print(f"Skills request failed: {skills_response.text}")
                else:
                    print("No token in login response")
            else:
                print("Login failed")
                
        except Exception as e:
            print(f"Login/test error: {e}")
        
        # Wait for more output
        time.sleep(2)
        
    except Exception as e:
        print(f"Test error: {e}")
    
    finally:
        print("\nTERMINATING BACKEND PROCESS...")
        process.terminate()
        time.sleep(1)
        process.kill()
        
        print("\n" + "="*60)
        print("TERMINAL OUTPUT CAPTURE COMPLETE!")
        print("="*60)
        
        print("\nEXPECTED ERROR TRACES TO LOOK FOR:")
        print("-" * 30)
        
        print("1. AUTHORIZATION ERRORS:")
        print("   - 'Authorization header required with Bearer token'")
        print("   - 'Invalid token'")
        print("   - 'Token has expired'")
        
        print("\n2. DATABASE ERRORS:")
        print("   - 'User not found in database'")
        print("   - 'Skill not found'")
        print("   - 'Cannot request your own skill'")
        
        print("\n3. VALIDATION ERRORS:")
        print("   - 'Message is required'")
        print("   - 'Skill ID is required'")
        
        print("\n4. INTERNAL ERRORS:")
        print("   - 'Unexpected error in direct_request_skill'")
        print("   - 'Notification creation failed'")
        print("   - 'Failed to create skill exchange request'")
        
        print("\n5. PYTHON TRACEBACK:")
        print("   - Look for 'Traceback (most recent call last):'")
        print("   - Check the exact line numbers and error messages")
        print("   - Note the exception type and details")
        
        print("\nWHAT TO DO WITH THIS OUTPUT:")
        print("-" * 30)
        print("1. Look for 'Traceback' in the backend output above")
        print("2. Identify the exact error line and message")
        print("3. Check if it's a database, validation, or import error")
        print("4. Note the specific exception type (e.g., AttributeError, KeyError)")
        print("5. Share the complete traceback for debugging")

if __name__ == "__main__":
    capture_backend_output()
