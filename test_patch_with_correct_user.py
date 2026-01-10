#!/usr/bin/env python3
"""
Test PATCH with Correct User Authorization
"""

import requests
import json

def test_patch_with_correct_user():
    """Test PATCH endpoint with user who owns the skill"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing PATCH with Correct User Authorization...')
    print('='*60)
    
    # Step 1: Get admin token
    print('1. Getting admin token...')
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = requests.post(base_url + '/admin/login', json=login_data, timeout=10)
        
        if response.ok:
            token = response.json().get('access_token')
            print('   SUCCESS: Got admin token')
        else:
            print(f'   ERROR: Failed to get token: {response.status_code}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 2: Get all requests to find one admin can update
    print('2. Getting exchange requests...')
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
        
        if response.ok:
            requests_data = response.json()
            print(f'   SUCCESS: Got {len(requests_data)} requests')
            
            # Find a request where admin is the skill owner
            admin_request = None
            for req in requests_data:
                if req.get('skill_owner', {}).get('username') == 'admin':
                    admin_request = req
                    break
            
            if admin_request:
                print(f'   Found request where admin is skill owner: ID {admin_request.get("id")}')
                print(f'   Current status: {admin_request.get("status")}')
                test_request_id = admin_request.get('id')
            else:
                print('   No requests found where admin is skill owner')
                print('   Creating a test request first...')
                
                # Create a test request
                skill_response = requests.get(base_url + '/api/skills/', headers=headers, timeout=10)
                if skill_response.ok:
                    skills = skill_response.json()
                    if skills:
                        # Find a skill owned by admin
                        admin_skill = None
                        for skill in skills:
                            if skill.get('owner', {}).get('username') == 'admin':
                                admin_skill = skill
                                break
                        
                        if admin_skill:
                            # Create a request for admin's skill
                            request_data = {
                                'skill_id': admin_skill['id'],
                                'message': 'Test request for PATCH endpoint'
                            }
                            create_response = requests.post(base_url + '/request-skill', 
                                                           json=request_data, 
                                                           headers=headers, 
                                                           timeout=10)
                            if create_response.ok:
                                new_request = create_response.json()
                                test_request_id = new_request.get('request_id')
                                print(f'   Created new request: ID {test_request_id}')
                            else:
                                print('   Failed to create test request')
                                return
                        else:
                            print('   No skills found owned by admin')
                            return
                    else:
                        print('   No skills found')
                        return
                else:
                    print('   Failed to get skills')
                    return
        else:
            print(f'   ERROR: Failed to get requests: {response.status_code}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 3: Test PATCH with correct authorization
    print('3. Testing PATCH with correct authorization...')
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        update_data = {'status': 'Accepted'}
        response = requests.patch(
            base_url + f'/api/exchanges/requests/{test_request_id}', 
            json=update_data, 
            headers=headers, 
            timeout=10
        )
        
        print(f'   Status Code: {response.status_code}')
        
        if response.ok:
            result = response.json()
            print('   SUCCESS: Request status updated')
            print(f'   Request ID: {result.get("request_id")}')
            print(f'   New Status: {result.get("status")}')
            print(f'   Message: {result.get("message")}')
        else:
            print(f'   ERROR: {response.status_code}')
            print(f'   Response Text: {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('PATCH with Correct User Testing Complete!')

if __name__ == "__main__":
    test_patch_with_correct_user()
