#!/usr/bin/env python3
"""
Test PATCH as Skill Owner
"""

import requests
import json

def test_patch_as_skill_owner():
    """Test PATCH endpoint as the actual skill owner"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing PATCH as Skill Owner...')
    print('='*50)
    
    # Step 1: Login as testuser (skill owner)
    print('1. Logging in as testuser (skill owner)...')
    try:
        login_data = {'username': 'testuser', 'password': 'password123'}
        response = requests.post(base_url + '/users/login', json=login_data, timeout=10)
        
        if response.ok:
            token = response.json().get('access_token')
            user_data = response.json()
            print(f'   SUCCESS: Logged in as {user_data.get("username")} (ID: {user_data.get("id")})')
        else:
            print(f'   ERROR: Failed to login: {response.status_code}')
            print(f'   Response: {response.text}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 2: Get testuser's requests
    print('2. Getting testuser requests...')
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(base_url + '/api/exchanges/', headers=headers, timeout=10)
        
        if response.ok:
            requests_data = response.json()
            print(f'   SUCCESS: Got {len(requests_data)} requests')
            
            # Find a pending request where testuser is skill owner
            pending_request = None
            for req in requests_data:
                if req.get('status') == 'pending' and req.get('skill_owner', {}).get('username') == 'testuser':
                    pending_request = req
                    break
            
            if pending_request:
                print(f'   Found pending request: ID {pending_request.get("id")}')
                print(f'   Skill: {pending_request.get("skill", {}).get("title")}')
                print(f'   Requester: {pending_request.get("requester", {}).get("username")}')
                test_request_id = pending_request.get('id')
            else:
                print('   No pending requests found where testuser is skill owner')
                return
        else:
            print(f'   ERROR: Failed to get requests: {response.status_code}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 3: Test PATCH as skill owner
    print('3. Testing PATCH as skill owner...')
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
            
            # Step 4: Verify the update
            print()
            print('4. Verifying the update...')
            verify_response = requests.get(base_url + '/api/exchanges/', headers=headers, timeout=10)
            
            if verify_response.ok:
                requests_data = verify_response.json()
                updated_request = None
                for req in requests_data:
                    if req.get('id') == test_request_id:
                        updated_request = req
                        break
                
                if updated_request:
                    print(f'   SUCCESS: Request {test_request_id} status is now: {updated_request.get("status")}')
                else:
                    print(f'   ERROR: Request {test_request_id} not found after update')
            else:
                print(f'   ERROR: Failed to verify: {verify_response.status_code}')
                
        else:
            print(f'   ERROR: {response.status_code}')
            print(f'   Response Text: {response.text}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('PATCH as Skill Owner Testing Complete!')

if __name__ == "__main__":
    test_patch_as_skill_owner()
