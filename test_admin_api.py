#!/usr/bin/env python3
"""
Test Admin Dashboard API Endpoints
"""

import requests

def test_admin_api():
    """Test all admin dashboard API endpoints"""
    base_url = 'http://127.0.0.1:8000'
    
    print('Testing Admin Dashboard API Endpoints:')
    print('='*50)
    
    # Test users endpoint
    print('1. Testing /users/ endpoint...')
    try:
        response = requests.get(f'{base_url}/users/', timeout=5)
        print(f'   Status: {response.status_code}')
        if response.ok:
            data = response.json()
            print(f'   Users Count: {len(data) if isinstance(data, list) else "Not a list"}')
            print(f'   Sample User: {data[0] if data and len(data) > 0 else "None"}')
        else:
            print(f'   Error: {response.text}')
    except Exception as e:
        print(f'   Exception: {e}')
    
    print()
    
    # Test skills endpoint
    print('2. Testing /api/skills/ endpoint...')
    try:
        response = requests.get(f'{base_url}/api/skills/', timeout=5)
        print(f'   Status: {response.status_code}')
        if response.ok:
            data = response.json()
            print(f'   Skills Count: {len(data) if isinstance(data, list) else "Not a list"}')
            print(f'   Sample Skill: {data[0] if data and len(data) > 0 else "None"}')
        else:
            print(f'   Error: {response.text}')
    except Exception as e:
        print(f'   Exception: {e}')
    
    print()
    
    # Test exchanges endpoint
    print('3. Testing /api/exchanges/ endpoint...')
    try:
        response = requests.get(f'{base_url}/api/exchanges/', timeout=5)
        print(f'   Status: {response.status_code}')
        if response.ok:
            data = response.json()
            print(f'   Requests Count: {len(data) if isinstance(data, list) else "Not a list"}')
            print(f'   Sample Request: {data[0] if data and len(data) > 0 else "None"}')
        else:
            print(f'   Error: {response.text}')
    except Exception as e:
        print(f'   Exception: {e}')
    
    print()
    print('API Endpoint Testing Complete!')

if __name__ == "__main__":
    test_admin_api()
