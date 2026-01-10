#!/usr/bin/env python3
"""
Test Backend on Port 8001
"""

import requests
import json

def test_backend_8001():
    """Test backend connection on port 8001"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing Backend on Port 8001...')
    print('='*40)
    
    # Test 1: Basic backend connection
    print('1. Testing basic backend connection...')
    try:
        response = requests.get(base_url + '/', timeout=10)
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            print('   SUCCESS: Backend is running on port 8001')
        else:
            print('   ERROR: Backend not responding correctly')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        print('   ERROR: Backend is not running on port 8001')
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
            print('   SUCCESS: Admin login working')
            print(f'   Token received: {len(data.get("access_token", ""))} characters')
            return data.get('access_token')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            return None
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return None

def test_dashboard_apis():
    """Test dashboard APIs with admin token"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('\nTesting Dashboard APIs...')
    print('='*30)
    
    # Get admin token
    print('Getting admin token...')
    try:
        response = requests.post(base_url + '/admin/login', 
                               json={'username': 'admin', 'password': 'admin123'}, 
                               timeout=10)
        
        if response.ok:
            data = response.json()
            admin_token = data['access_token']
            print('   SUCCESS: Got admin token')
        else:
            print('   ERROR: Failed to get token')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Test skills endpoint
    print('Testing /api/skills/ endpoint...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(base_url + '/api/skills/', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} skills')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test exchanges/all endpoint
    print('Testing /api/exchanges/all endpoint...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} exchange requests')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')

if __name__ == "__main__":
    test_backend_8001()
    test_dashboard_apis()
