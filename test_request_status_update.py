#!/usr/bin/env python3
"""
Test Request Status Update API
"""

import requests
import json

def test_request_status_update():
    """Test PATCH /api/exchanges/requests/:id endpoint"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing Request Status Update API...')
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
    
    # Step 2: Get some requests
    print('2. Getting exchange requests...')
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(base_url + '/api/exchanges/all', headers=headers, timeout=10)
        
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
    
    # Step 3: Test status update
    print('3. Testing status update...')
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Test accepting a request
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
    
    # Step 4: Test invalid status
    print('4. Testing invalid status...')
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        update_data = {'status': 'InvalidStatus'}
        response = requests.patch(
            base_url + f'/api/exchanges/requests/{test_request_id}', 
            json=update_data, 
            headers=headers, 
            timeout=10
        )
        
        print(f'   Status Code: {response.status_code}')
        
        if response.status_code == 400:
            print('   SUCCESS: Invalid status properly rejected')
        else:
            print(f'   ERROR: Expected 400, got {response.status_code}')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Request Status Update Testing Complete!')

if __name__ == "__main__":
    test_request_status_update()
