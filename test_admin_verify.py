#!/usr/bin/env python3
"""
Test Admin Verify Endpoint
"""

import requests
import json

def test_admin_verify():
    """Test admin verify endpoint with different approaches"""
    
    base_url = 'http://127.0.0.1:8000'
    
    print('Testing Admin Verify Endpoint...')
    print('='*40)
    
    # Step 1: Get admin token
    print('1. Getting admin token...')
    try:
        response = requests.post(f'{base_url}/admin/login', json={
            'username': 'admin',
            'password': 'admin123'
        }, timeout=10)
        
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
    
    # Step 2: Test with Authorization header
    print('2. Testing with Authorization header...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(f'{base_url}/admin/verify', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        print(f'   Headers sent: {headers}')
        print(f'   Response: {response.text}')
        
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 3: Test with query parameter (alternative)
    print('3. Testing with query parameter...')
    try:
        response = requests.get(f'{base_url}/admin/verify?token={admin_token}', timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        print(f'   Response: {response.text}')
        
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 4: Check if endpoint exists
    print('4. Checking if endpoint exists...')
    try:
        response = requests.get(f'{base_url}/admin/verify', timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        print(f'   Response: {response.text}')
        
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 5: Check admin endpoints list
    print('5. Checking available admin endpoints...')
    try:
        response = requests.get(f'{base_url}/docs', timeout=10)
        
        if response.ok:
            if 'admin' in response.text.lower():
                print('   SUCCESS: Admin endpoints found in docs')
                # Look for verify endpoint
                if 'verify' in response.text.lower():
                    print('   SUCCESS: Verify endpoint found in docs')
                else:
                    print('   WARNING: Verify endpoint not found in docs')
            else:
                print('   WARNING: Admin endpoints not found in docs')
        else:
            print(f'   ERROR: Could not access docs - {response.status_code}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Admin Verify Testing Complete!')

if __name__ == "__main__":
    test_admin_verify()
