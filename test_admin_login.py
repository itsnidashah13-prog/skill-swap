#!/usr/bin/env python3
"""
Test Admin Login
"""

import requests
import json

def test_admin_login():
    """Test admin login with both username and email"""
    
    base_url = 'http://127.0.0.1:8000'
    
    print('Testing Admin Login...')
    print('='*40)
    
    # Test 1: Login with username
    print('1. Testing login with username "admin"...')
    try:
        response = requests.post(f'{base_url}/admin/login', json={
            'username': 'admin',
            'password': 'admin123'
        }, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print('   SUCCESS: Login with username works!')
            print(f'   Token Type: {data.get("token_type")}')
            print(f'   Expires In: {data.get("expires_in")} seconds')
            print(f'   Admin User: {data.get("admin_user", {}).get("username")} ({data.get("admin_user", {}).get("email")})')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 2: Login with email
    print('2. Testing login with email "admin@example.com"...')
    try:
        response = requests.post(f'{base_url}/admin/login', json={
            'username': 'admin@example.com',
            'password': 'admin123'
        }, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            data = response.json()
            print('   SUCCESS: Login with email works!')
            print(f'   Token Type: {data.get("token_type")}')
            print(f'   Expires In: {data.get("expires_in")} seconds')
            print(f'   Admin User: {data.get("admin_user", {}).get("username")} ({data.get("admin_user", {}).get("email")})')
        else:
            print(f'   ERROR: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 3: Test wrong password
    print('3. Testing login with wrong password...')
    try:
        response = requests.post(f'{base_url}/admin/login', json={
            'username': 'admin',
            'password': 'wrongpassword'
        }, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.status_code == 401:
            print('   SUCCESS: Wrong password correctly rejected')
        else:
            print(f'   ERROR: Expected 401, got {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 4: Test non-admin user
    print('4. Testing login with non-admin user...')
    try:
        response = requests.post(f'{base_url}/admin/login', json={
            'username': 'testuser',
            'password': 'test123'
        }, timeout=10)
        
        print(f'   Status Code: {response.status_code}')
        
        if response.status_code == 401 or response.status_code == 403:
            print('   SUCCESS: Non-admin user correctly rejected')
        else:
            print(f'   ERROR: Expected 401/403, got {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')

if __name__ == "__main__":
    test_admin_login()
