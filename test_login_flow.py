#!/usr/bin/env python3
"""
Test Complete Login Flow
"""

import requests
import json

def test_login_flow():
    """Test complete login flow from login to dashboard"""
    
    base_url = 'http://127.0.0.1:8001'
    login_url = 'http://127.0.0.1:3006/admin_login_simple.html'
    dashboard_url = 'http://127.0.0.1:3008/admin_simple.html'
    
    print('Testing Complete Login Flow...')
    print('='*40)
    
    # Step 1: Test admin login
    print('1. Testing admin login...')
    try:
        response = requests.post(base_url + '/admin/login', 
                               json={'username': 'admin', 'password': 'admin123'}, 
                               timeout=10)
        
        if response.ok:
            data = response.json()
            admin_token = data['access_token']
            print(f'   SUCCESS: Got admin token')
            print(f'   Token: {admin_token[:50]}...')
            print(f'   Admin User: {data.get("admin_user", {}).get("username")}')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 2: Test admin verify
    print('2. Testing admin verify...')
    try:
        headers = {'Authorization': f'Bearer {admin_token}'}
        response = requests.get(base_url + '/admin/verify', headers=headers, timeout=10)
        
        if response.ok:
            data = response.json()
            print('   SUCCESS: Admin token verified')
            print(f'   Valid: {data.get("valid")}')
            print(f'   Username: {data.get("username")}')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 3: Test skills API with token
    print('3. Testing skills API with token...')
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Origin': 'http://127.0.0.1:3008'
        }
        response = requests.get(base_url + '/api/skills/', headers=headers, timeout=10)
        
        if response.ok:
            data = response.json()
            print(f'   SUCCESS: Got {len(data)} skills')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 4: Test CORS headers
    print('4. Testing CORS headers...')
    try:
        headers = {
            'Origin': 'http://127.0.0.1:3008',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }
        
        response = requests.options(base_url + '/api/skills/', headers=headers, timeout=10)
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
            print('   SUCCESS: CORS is configured for port 3008')
        else:
            print('   WARNING: CORS headers not found for port 3008')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Step 5: Check URLs
    print('5. URL Configuration Check:')
    print(f'   Backend URL: {base_url}')
    print(f'   Login Page: {login_url}')
    print(f'   Dashboard URL: {dashboard_url}')
    print(f'   CORS Origins: http://127.0.0.1:3008, http://localhost:3008')
    
    print()
    print('Login Flow Testing Complete!')
    print()
    print('NEXT STEPS:')
    print('1. Open login page: http://127.0.0.1:3006/admin_login_simple.html')
    print('2. Enter credentials: admin / admin123')
    print('3. After login, you will be redirected to: http://127.0.0.1:3008/admin_simple.html')
    print('4. Dashboard should automatically load with your admin token')

if __name__ == "__main__":
    test_login_flow()
