#!/usr/bin/env python3
"""
Test Dashboard APIs with Fixed Endpoints
"""

import requests
import json

def test_dashboard_fixed():
    """Test all dashboard APIs with admin authentication"""
    
    base_url = 'http://127.0.0.1:8000'
    
    print('Testing Fixed Dashboard APIs...')
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
    
    # Step 4: Test exchanges/all endpoint (fixed)
    print('4. Testing /api/exchanges/all endpoint (fixed)...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(f'{base_url}/api/exchanges/all', headers=headers, timeout=10)
        
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
    
    # Step 5: Test old exchanges endpoint (for comparison)
    print('5. Testing old /api/exchanges/ endpoint...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(f'{base_url}/api/exchanges/', headers=headers, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} exchange requests')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Fixed Dashboard API Testing Complete!')

if __name__ == "__main__":
    test_dashboard_fixed()
