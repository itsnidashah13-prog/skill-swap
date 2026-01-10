#!/usr/bin/env python3
"""
Test Backend Connection and CORS
"""

import requests
import json

def test_backend_connection():
    """Test backend connection and CORS"""
    
    base_url = 'http://127.0.0.1:8000'
    
    print('Testing Backend Connection...')
    print('='*40)
    
    # Test 1: Basic backend connection
    print('1. Testing basic backend connection...')
    try:
        response = requests.get(base_url + '/', timeout=10)
        print(f'   Status Code: {response.status_code}')
        print(f'   Response: {response.text[:100]}...')
        
        if response.ok:
            print('   SUCCESS: Backend is running')
        else:
            print('   ERROR: Backend not responding correctly')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        print('   ERROR: Backend is not running or not accessible')
        return
    
    print()
    
    # Test 2: Admin login endpoint
    print('2. Testing admin login endpoint...')
    try:
        response = requests.post(base_url + '/admin/login', 
                               json={'username': 'admin', 'password': 'admin123'}, 
                               timeout=10)
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print('   SUCCESS: Admin login endpoint working')
            print(f'   Token received: {len(data.get("access_token", ""))} characters')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 3: CORS headers
    print('3. Testing CORS headers...')
    try:
        # Simulate a request from admin dashboard
        headers = {
            'Origin': 'http://127.0.0.1:3007',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }
        
        response = requests.options(base_url + '/admin/login', headers=headers, timeout=10)
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
    
    # Test 4: Skills endpoint
    print('4. Testing skills endpoint...')
    try:
        # First get admin token
        login_response = requests.post(base_url + '/admin/login', 
                                    json={'username': 'admin', 'password': 'admin123'}, 
                                    timeout=10)
        
        if login_response.ok:
            token = login_response.json().get('access_token')
            
            # Test skills endpoint with token
            headers = {
                'Authorization': f'Bearer {token}',
                'Origin': 'http://127.0.0.1:3007'
            }
            
            response = requests.get(base_url + '/api/skills/', headers=headers, timeout=10)
            print(f'   Status Code: {response.status_code}')
            
            if response.ok:
                data = response.json()
                print(f'   SUCCESS: Got {len(data)} skills')
            else:
                print(f'   ERROR: {response.status_code} - {response.text}')
        else:
            print('   ERROR: Could not get admin token')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 5: Exchanges all endpoint
    print('5. Testing exchanges/all endpoint...')
    try:
        # Get admin token again
        login_response = requests.post(base_url + '/admin/login', 
                                    json={'username': 'admin', 'password': 'admin123'}, 
                                    timeout=10)
        
        if login_response.ok:
            token = login_response.json().get('access_token')
            
            # Test exchanges/all endpoint with token
            headers = {
                'Authorization': f'Bearer {token}',
                'Origin': 'http://127.0.0.1:3007'
            }
            
            response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
            print(f'   Status Code: {response.status_code}')
            
            if response.ok:
                data = response.json()
                print(f'   SUCCESS: Got {len(data)} exchange requests')
            else:
                print(f'   ERROR: {response.status_code} - {response.text}')
        else:
            print('   ERROR: Could not get admin token')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Backend Connection Testing Complete!')

if __name__ == "__main__":
    test_backend_connection()
