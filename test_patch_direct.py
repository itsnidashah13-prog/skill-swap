#!/usr/bin/env python3
"""
Test PATCH endpoint directly
"""

import requests
import json

def test_patch_direct():
    """Test PATCH endpoint with a specific request ID"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing PATCH Endpoint Directly...')
    print('='*50)
    
    # Get admin token
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = requests.post(base_url + '/admin/login', json=login_data, timeout=10)
        
        if response.ok:
            token = response.json().get('access_token')
            print('SUCCESS: Got admin token')
        else:
            print(f'ERROR: Failed to get token: {response.status_code}')
            return
            
    except Exception as e:
        print(f'EXCEPTION: {e}')
        return
    
    print()
    
    # Test PATCH endpoint with a sample request ID
    print('Testing PATCH endpoint with request ID 1...')
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        update_data = {'status': 'Accepted'}
        response = requests.patch(
            base_url + '/api/exchanges/requests/1', 
            json=update_data, 
            headers=headers, 
            timeout=10
        )
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Headers: {dict(response.headers)}')
        print(f'Response Text: {response.text}')
        
        if response.ok:
            result = response.json()
            print('SUCCESS: PATCH endpoint working')
            print(f'Request ID: {result.get("request_id")}')
            print(f'New Status: {result.get("status")}')
        else:
            print(f'ERROR: {response.status_code}')
            
    except Exception as e:
        print(f'EXCEPTION: {e}')
    
    print()
    print('Direct PATCH Testing Complete!')

if __name__ == "__main__":
    test_patch_direct()
