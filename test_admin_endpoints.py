#!/usr/bin/env python3
"""
Test Backend Admin Endpoints
"""

import requests
import base64

def test_admin_endpoints():
    """Test all admin endpoints"""
    base_url = 'http://127.0.0.1:8000'

    print('Testing Backend Admin Endpoints:')
    print('='*50)

    # Test admin login page
    print('1. Testing /admin/login endpoint...')
    try:
        response = requests.get(f'{base_url}/admin/login', timeout=5)
        print(f'   Status: {response.status_code}')
        print(f'   Content-Type: {response.headers.get("Content-Type", "Not found")}')
        if response.status_code == 200:
            print('   Result: Admin login page accessible')
        else:
            print(f'   Error: {response.text[:200]}')
    except Exception as e:
        print(f'   Exception: {e}')

    print()

    # Test admin dashboard (should redirect to login)
    print('2. Testing /admin/ endpoint (without auth)...')
    try:
        response = requests.get(f'{base_url}/admin/', timeout=5)
        print(f'   Status: {response.status_code}')
        if response.status_code == 302:
            print('   Result: Correctly redirects to login (302)')
            print(f'   Redirect to: {response.headers.get("Location", "Not found")}')
        else:
            print(f'   Response: {response.text[:200]}')
    except Exception as e:
        print(f'   Exception: {e}')

    print()

    # Test admin dashboard with Basic Auth
    print('3. Testing /admin/ endpoint with Basic Auth...')
    try:
        credentials = base64.b64encode(b'admin:admin123').decode()
        headers = {'Authorization': f'Basic {credentials}'}
        response = requests.get(f'{base_url}/admin/', headers=headers, timeout=5)
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            print('   Result: Admin dashboard accessible with Basic Auth')
        else:
            print(f'   Error: {response.text[:200]}')
    except Exception as e:
        print(f'   Exception: {e}')

    print()

    # Test if admin router is included
    print('4. Testing admin router inclusion...')
    try:
        response = requests.get(f'{base_url}/docs', timeout=5)
        if response.status_code == 200:
            print('   Result: Swagger docs accessible')
            # Check if admin endpoints are listed
            if 'admin' in response.text.lower():
                print('   Status: Admin endpoints found in docs')
            else:
                print('   Status: Admin endpoints NOT found in docs')
        else:
            print(f'   Error: {response.status_code}')
    except Exception as e:
        print(f'   Exception: {e}')

    print()
    print('Backend Admin Endpoint Testing Complete!')

if __name__ == "__main__":
    test_admin_endpoints()
