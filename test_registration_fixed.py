#!/usr/bin/env python3
"""
Test Registration API Fixed
"""

import requests
import json

def test_registration_fixed():
    """Test registration API with correct URL"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing Registration API (Fixed)...')
    print('='*50)
    
    # Test 1: Registration with correct URL
    print('1. Testing user registration with correct URL...')
    try:
        registration_data = {
            'username': 'testuser_fixed',
            'email': 'testuser_fixed@example.com',
            'password': 'testpass123',
            'full_name': 'Test User Fixed',
            'bio': 'Test user for registration fix verification'
        }
        
        # Test both URLs to find the correct one
        urls_to_test = [
            '/users/register',
            '/api/users/register'
        ]
        
        for url in urls_to_test:
            print(f'   Testing URL: {base_url}{url}')
            response = requests.post(base_url + url, 
                                   json=registration_data, 
                                   timeout=10)
            
            print(f'   Status Code: {response.status_code}')
            
            if response.ok:
                data = response.json()
                print('   SUCCESS: User registered successfully')
                print(f'   User ID: {data.get("id")}')
                print(f'   Username: {data.get("username")}')
                print(f'   Email: {data.get("email")}')
                print(f'   Full Name: {data.get("full_name")}')
                break
            else:
                print(f'   ERROR: {response.status_code}')
                print(f'   Response Text: {response.text}')
            
            print()
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 2: Test frontend getApiUrl function
    print('2. Testing frontend getApiUrl function...')
    try:
        # Simulate getApiUrl function
        API_BASE_URL = 'http://127.0.0.1:8001'
        
        def getApiUrl(endpoint):
            cleanEndpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
            if not cleanEndpoint.startswith('api/'):
                return f'{API_BASE_URL}/api/{cleanEndpoint}'
            return f'{API_BASE_URL}/{cleanEndpoint}'
        
        # Test both endpoints
        test_endpoints = ['users/register', 'users/login']
        
        for endpoint in test_endpoints:
            url = getApiUrl(endpoint)
            print(f'   getApiUrl("{endpoint}") = {url}')
            
            # Test if URL exists
            try:
                response = requests.options(url, timeout=5)
                print(f'   OPTIONS Status: {response.status_code}')
            except:
                print(f'   OPTIONS Status: Failed (endpoint may not exist)')
        
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Registration Fixed Testing Complete!')

if __name__ == "__main__":
    test_registration_fixed()
