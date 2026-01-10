#!/usr/bin/env python3
"""
Debug Backend Error
"""

import requests
import json

def debug_backend_error():
    """Debug backend error with detailed logging"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Debugging Backend Error...')
    print('='*30)
    
    # Get admin token
    try:
        response = requests.post(base_url + '/admin/login', 
                               json={'username': 'admin', 'password': 'admin123'}, 
                               timeout=10)
        
        if response.ok:
            data = response.json()
            admin_token = data['access_token']
            print(f'Got admin token: {admin_token[:50]}...')
        else:
            print(f'Failed to get token: {response.status_code}')
            return
            
    except Exception as e:
        print(f'Exception getting token: {e}')
        return
    
    print()
    
    # Test with detailed error capture
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        print('Making request to /api/exchanges/all...')
        print(f'Headers: {headers}')
        
        response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Headers: {dict(response.headers)}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 500:
            print('500 Internal Server Error detected!')
            print('This suggests a backend code issue, not authentication.')
            
    except Exception as e:
        print(f'Request exception: {e}')
    
    print()
    
    # Test skills endpoint for comparison
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        print('Making request to /api/skills/ for comparison...')
        response = requests.get(base_url + '/api/skills/', headers=headers, timeout=10)
        
        print(f'Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'Skills endpoint working: {len(data)} skills returned')
        else:
            print(f'Skills endpoint also failing: {response.status_code}')
            
    except Exception as e:
        print(f'Skills request exception: {e}')

if __name__ == "__main__":
    debug_backend_error()
