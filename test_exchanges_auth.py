#!/usr/bin/env python3
"""
Test Exchanges API with Authentication
"""

import requests
import json

def test_exchanges_auth():
    """Test exchanges API with proper authentication"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing Exchanges API with Authentication...')
    print('='*50)
    
    # Step 1: Get admin token
    print('1. Getting admin token...')
    try:
        response = requests.post(base_url + '/admin/login', 
                               json={'username': 'admin', 'password': 'admin123'}, 
                               timeout=10)
        
        if response.ok:
            data = response.json()
            admin_token = data['access_token']
            print(f'   SUCCESS: Got admin token')
            print(f'   Token: {admin_token[:50]}...')
        else:
            print(f'   ERROR: Failed to get token - {response.status_code}')
            return None
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return None
    
    print()
    
    # Step 2: Test /api/exchanges/all with proper headers
    print('2. Testing /api/exchanges/all with Bearer token...')
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json',
            'Origin': 'http://127.0.0.1:3008'
        }
        
        print(f'   Headers being sent:')
        for key, value in headers.items():
            print(f'     {key}: {value}')
        
        response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        print(f'   Response Headers: {dict(response.headers)}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} exchange requests')
            if len(data) > 0:
                print(f'   Sample request keys: {list(data[0].keys()) if data else "No data"}')
        else:
            print(f'   ERROR: {response.status_code}')
            print(f'   Response Text: {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 3: Test /api/exchanges/ (user endpoint)
    print('3. Testing /api/exchanges/ (user endpoint) with admin token...')
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json',
            'Origin': 'http://127.0.0.1:3008'
        }
        
        response = requests.get(base_url + '/api/exchanges/', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} exchange requests')
        else:
            print(f'   ERROR: {response.status_code}')
            print(f'   Response Text: {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 4: Test without authentication
    print('4. Testing /api/exchanges/all without authentication...')
    try:
        response = requests.get(base_url + '/api/exchanges/all', timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.status_code == 401:
            print('   SUCCESS: Correctly requires authentication')
        else:
            print(f'   ERROR: Expected 401, got {response.status_code}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 5: Test with invalid token
    print('5. Testing /api/exchanges/all with invalid token...')
    try:
        headers = {
            'Authorization': 'Bearer invalid_token_here',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.status_code == 401:
            print('   SUCCESS: Correctly rejects invalid token')
        else:
            print(f'   ERROR: Expected 401, got {response.status_code}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Exchanges API Authentication Testing Complete!')

if __name__ == "__main__":
    test_exchanges_auth()
