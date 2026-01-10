#!/usr/bin/env python3
"""
Test PATCH Working Endpoint
"""

import requests
import json

def test_patch_working():
    """Test PATCH endpoint using working user endpoint"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing PATCH Working Endpoint...')
    print('='*50)
    
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
    
    # Step 2: Get admin's requests using user endpoint
    print('2. Getting admin requests...')
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(base_url + '/api/exchanges/', headers=headers, timeout=10)
        
        if response.ok:
            requests_data = response.json()
            print(f'   SUCCESS: Got {len(requests_data)} requests')
            
            if requests_data:
                # Find a pending request
                pending_request = None
                for req in requests_data:
                    if req.get('status') == 'pending':
                        pending_request = req
                        break
                
                if pending_request:
                    print(f'   Found pending request: ID {pending_request.get("id")}')
                    print(f'   Skill: {pending_request.get("skill", {}).get("title")}')
                    test_request_id = pending_request.get('id')
                else:
                    print('   No pending requests found, using first request')
                    test_request_id = requests_data[0].get('id')
            else:
                print('   No requests found')
                return
        else:
            print(f'   ERROR: Failed to get requests: {response.status_code}')
            return
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
        return
    
    print()
    
    # Step 3: Test PATCH endpoint
    print('3. Testing PATCH endpoint...')
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
        print(f'   Response Headers: {dict(response.headers)}')
        
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
    
    # Step 4: Verify the update
    print('4. Verifying the update...')
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(base_url + '/api/exchanges/', headers=headers, timeout=10)
        
        if response.ok:
            requests_data = response.json()
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
            print(f'   ERROR: Failed to verify: {response.status_code}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('PATCH Working Testing Complete!')

if __name__ == "__main__":
    test_patch_working()
