v#!/usr/bin/env python3
"""
Debug Exchanges All Endpoint
"""

import requests
import json

def debug_exchanges_endpoint():
    """Debug the exchanges/all endpoint with detailed error handling"""
    
    base_url = 'http://127.0.0.1:8000'
    
    print('Debugging Exchanges All Endpoint...')
    print('='*40)
    
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
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 2: Test exchanges/all endpoint with detailed error capture
    print('2. Testing exchanges/all endpoint...')
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
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
            
            # Try to parse error details
            try:
                error_data = response.json()
                print(f'   Error Details: {error_data}')
            except:
                print(f'   Raw Error: {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 3: Test regular exchanges endpoint for comparison
    print('3. Testing regular exchanges endpoint...')
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
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
    print('4. Testing exchanges/all without authentication...')
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
    print('Exchanges Endpoint Debug Complete!')

if __name__ == "__main__":
    debug_exchanges_endpoint()
