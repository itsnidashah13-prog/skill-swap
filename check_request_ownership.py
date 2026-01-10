#!/usr/bin/env python3
"""
Check Request Ownership
"""

import requests
import json

def check_request_ownership():
    """Check who owns the skill in request 126"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Checking Request Ownership...')
    print('='*40)
    
    # Get admin token
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = requests.post(base_url + '/admin/login', json=login_data, timeout=10)
        
        if response.ok:
            token = response.json().get('access_token')
            print('Got admin token')
        else:
            print(f'Failed to get token: {response.status_code}')
            return
            
    except Exception as e:
        print(f'Exception: {e}')
        return
    
    print()
    
    # Get admin's requests
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(base_url + '/api/exchanges/', headers=headers, timeout=10)
        
        if response.ok:
            requests_data = response.json()
            print(f'Admin has {len(requests_data)} requests:')
            
            for req in requests_data:
                print(f'  Request ID: {req.get("id")}')
                print(f'  Skill: {req.get("skill", {}).get("title")}')
                print(f'  Requester: {req.get("requester", {}).get("username")} (ID: {req.get("requester_id")})')
                print(f'  Skill Owner: {req.get("skill_owner", {}).get("username")} (ID: {req.get("skill_owner_id")})')
                print(f'  Status: {req.get("status")}')
                print(f'  Admin ID: 40')
                print(f'  Is admin skill owner? {req.get("skill_owner_id") == 40}')
                print()
        else:
            print(f'Failed to get requests: {response.status_code}')
            
    except Exception as e:
        print(f'Exception: {e}')

if __name__ == "__main__":
    check_request_ownership()
