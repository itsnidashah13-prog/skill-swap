#!/usr/bin/env python3
"""
Test Registration API
"""

import requests
import json

def test_registration():
    """Test registration API on port 8001"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing Registration API...')
    print('='*40)
    
    # Test 1: Basic registration
    print('1. Testing user registration...')
    try:
        registration_data = {
            'username': 'testuser_new',
            'email': 'testuser_new@example.com',
            'password': 'testpass123',
            'full_name': 'Test User New',
            'bio': 'Test user for registration'
        }
        
        response = requests.post(base_url + '/api/users/register', 
                               json=registration_data, 
                               timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        print(f'   Response Headers: {dict(response.headers)}')
        
        if response.ok:
            data = response.json()
            print('   SUCCESS: User registered successfully')
            print(f'   User ID: {data.get("id")}')
            print(f'   Username: {data.get("username")}')
        else:
            print(f'   ERROR: {response.status_code}')
            print(f'   Response Text: {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 2: Check CORS headers
    print('2. Testing CORS headers for registration...')
    try:
        headers = {
            'Origin': 'http://127.0.0.1:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(base_url + '/api/users/register', headers=headers, timeout=10)
        print(f'   OPTIONS Status Code: {response.status_code}')
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
        }
        
        print('   CORS Headers:')
        for key, value in cors_headers.items():
            if value:
                print(f'     {key}: {value}')
        
        if cors_headers['Access-Control-Allow-Origin']:
            print('   SUCCESS: CORS is configured')
        else:
            print('   WARNING: CORS headers not found')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 3: Test skill request (to check skill.user fix)
    print('3. Testing skill request (checking skill.user fix)...')
    try:
        # First login to get token
        login_data = {'username': 'admin', 'password': 'admin123'}
        login_response = requests.post(base_url + '/admin/login', 
                                   json=login_data, 
                                   timeout=10)
        
        if login_response.ok:
            token = login_response.json().get('access_token')
            print('   SUCCESS: Got admin token')
            
            # Test skill request
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            skill_request_data = {
                'skill_id': 1,
                'message': 'Test skill request after fix'
            }
            
            response = requests.post(base_url + '/request-skill', 
                                   json=skill_request_data, 
                                   headers=headers, 
                                   timeout=10)
            
            print(f'   Status Code: {response.status_code}')
            
            if response.ok:
                data = response.json()
                print('   SUCCESS: Skill request created')
                print(f'   Request ID: {data.get("request_id")}')
                print(f'   Skill Owner: {data.get("skill_owner")}')
            else:
                print(f'   ERROR: {response.status_code}')
                print(f'   Response Text: {response.text}')
        else:
            print('   ERROR: Could not get admin token')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Registration Testing Complete!')

if __name__ == "__main__":
    test_registration()
