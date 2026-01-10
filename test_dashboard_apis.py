#!/usr/bin/env python3
"""
Test Dashboard APIs with Admin Token
"""

import requests
import json

def test_dashboard_apis():
    """Test all dashboard APIs with admin authentication"""
    
    base_url = 'http://127.0.0.1:8000'
    
    print('Testing Dashboard APIs with Admin Token...')
    print('='*50)
    
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
            print(f'   Response: {response.text}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 2: Test admin verify endpoint
    print('2. Testing admin verify endpoint...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(f'{base_url}/admin/verify', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print('   SUCCESS: Admin token verified')
            print(f'   User: {data.get("username")} ({data.get("email")})')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 3: Test skills endpoint
    print('3. Testing /api/skills/ endpoint...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(f'{base_url}/api/skills/', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} skills')
            if len(data) > 0:
                print(f'   Sample skill: {data[0].get("title", "N/A")}')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 4: Test exchanges endpoint
    print('4. Testing /api/exchanges/ endpoint...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(f'{base_url}/api/exchanges/', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} exchange requests')
            if len(data) > 0:
                print(f'   Sample request: {data[0].get("skill", {}).get("title", "N/A")}')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 5: Test without token (should fail)
    print('5. Testing APIs without token (should fail)...')
    try:
        response = requests.get(f'{base_url}/api/skills/', timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.status_code == 401:
            print('   SUCCESS: APIs correctly reject unauthenticated requests')
        else:
            print(f'   ERROR: Expected 401, got {response.status_code}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Dashboard API Testing Complete!')

if __name__ == "__main__":
    test_dashboard_apis()
