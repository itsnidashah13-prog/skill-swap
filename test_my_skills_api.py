#!/usr/bin/env python3
"""
Test script to verify My Skills API endpoint
"""

import requests
import json

# API base URL
API_BASE_URL = "http://127.0.0.1:8001"

def test_my_skills_endpoint():
    """Test the GET /api/skills/my-skills endpoint"""
    
    print("Testing My Skills API Endpoint")
    print("=" * 50)
    
    # First, login to get a valid token
    print("1. Testing login to get token...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(
            f"{API_BASE_URL}/users/login",
            json=login_data  # Using JSON data
        )
        
        print(f"   Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"   Token received: {access_token[:20] if access_token else 'None'}...")
            
            # Now test the my-skills endpoint
            print("\n2. Testing GET /api/skills/my-skills...")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            skills_response = requests.get(
                f"{API_BASE_URL}/api/skills/my-skills",
                headers=headers
            )
            
            print(f"   Skills Status: {skills_response.status_code}")
            print(f"   Response Headers: {dict(skills_response.headers)}")
            
            if skills_response.status_code == 200:
                skills_data = skills_response.json()
                print(f"   Skills loaded successfully!")
                print(f"   Skills count: {len(skills_data)}")
                print(f"   Skills data: {json.dumps(skills_data, indent=2)}")
                
                return True
            else:
                print(f"   Failed to load skills")
                print(f"   Error response: {skills_response.text}")
                return False
                
        else:
            print(f"   Login failed")
            print(f"   Error response: {login_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   Connection error - backend may not be running")
        return False
    except Exception as e:
        print(f"   Unexpected error: {e}")
        return False

def test_endpoint_without_token():
    """Test the endpoint without authentication"""
    print("\n3. Testing endpoint without token...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/skills/my-skills")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("   Correctly requires authentication")
            return True
        else:
            print("   Should require authentication")
            return False
            
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_endpoint_with_invalid_token():
    """Test the endpoint with invalid token"""
    print("\n4. Testing endpoint with invalid token...")
    
    headers = {
        "Authorization": "Bearer invalid-token-here",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/skills/my-skills", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("   Correctly rejects invalid token")
            return True
        else:
            print("   Should reject invalid token")
            return False
            
    except Exception as e:
        print(f"   Error: {e}")
        return False

if __name__ == "__main__":
    print("My Skills API Test")
    print("=" * 50)
    
    # Test the endpoint
    success = test_my_skills_endpoint()
    test_endpoint_without_token()
    test_endpoint_with_invalid_token()
    
    print("\n" + "=" * 50)
    if success:
        print("My Skills API is working correctly!")
    else:
        print("My Skills API has issues that need to be fixed")
    
    print("\nDebugging Checklist:")
    print("1. Backend is running on port 8001")
    print("2. Database connection is working")
    print("3. User 'testuser' exists in database")
    print("4. Authentication system is working")
    print("5. API endpoint is correctly configured")
