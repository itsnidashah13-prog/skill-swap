#!/usr/bin/env python3
"""
Test script to verify backend fixes
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint, method="GET", data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return False
            
        print(f"\n{'='*50}")
        print(f"TEST: {method} {endpoint}")
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        if response.status_code < 400:
            print("✅ SUCCESS")
            return True
        else:
            print("❌ FAILED")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n{'='*50}")
        print(f"TEST: {method} {endpoint}")
        print(f"❌ CONNECTION ERROR: {e}")
        return False

def main():
    print("🔍 TESTING BACKEND FIXES")
    print("="*60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Root endpoint
    total_tests += 1
    if test_endpoint("/"):
        tests_passed += 1
    
    # Test 2: Health check
    total_tests += 1
    if test_endpoint("/health"):
        tests_passed += 1
    
    # Test 3: Debug endpoints
    total_tests += 1
    if test_endpoint("/debug/endpoints"):
        tests_passed += 1
    
    total_tests += 1
    if test_endpoint("/debug/cors"):
        tests_passed += 1
    
    total_tests += 1
    if test_endpoint("/debug/database"):
        tests_passed += 1
    
    # Test 4: API endpoints
    total_tests += 1
    if test_endpoint("/api/skills/"):
        tests_passed += 1
    
    # Test 5: User registration
    total_tests += 1
    user_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "full_name": "Test User",
        "password": "password123",
        "bio": "Test user for backend verification"
    }
    if test_endpoint("/api/users/register", "POST", user_data):
        tests_passed += 1
    
    # Test 6: User login
    total_tests += 1
    login_data = {
        "username": "testuser123",
        "password": "password123"
    }
    login_result = test_endpoint("/api/users/login", "POST", login_data)
    if login_result:
        tests_passed += 1
        
        # Test 7: Get current user (with token)
        # Extract token from login response (this is simplified)
        print("\n🔑 Note: For authenticated endpoints, you'll need to extract the token from login response")
    
    # Test 8: CORS preflight
    total_tests += 1
    headers = {
        "Origin": "http://127.0.0.1:3002",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Authorization, Content-Type"
    }
    if test_endpoint("/api/exchanges/", "OPTIONS", headers=headers):
        tests_passed += 1
    
    # Results
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Backend is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
