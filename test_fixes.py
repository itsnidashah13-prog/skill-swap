#!/usr/bin/env python3
"""
Test script to verify the skills endpoint fixes
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("=== Testing Community Skill Swap API ===\n")
    
    # Test 1: Register a test user
    print("1. Testing user registration...")
    try:
        register_data = {
            "username": "testuser_debug",
            "email": "testdebug@example.com", 
            "full_name": "Test Debug User",
            "password": "password123",
            "bio": "Debug test user"
        }
        response = requests.post(f"{API_BASE_URL}/users/register", json=register_data)
        if response.status_code == 201:
            print("SUCCESS: Registration successful")
        else:
            print(f"WARNING: Registration: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: Registration error: {e}")
    
    # Test 2: Login
    print("\n2. Testing user login...")
    try:
        login_data = {"username": "testuser_debug", "password": "password123"}
        response = requests.post(f"{API_BASE_URL}/users/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("SUCCESS: Login successful")
            print(f"Token: {token[:50]}...")
        else:
            print(f"ERROR: Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"ERROR: Login error: {e}")
        return
    
    # Test 3: Create a skill
    print("\n3. Testing skill creation...")
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        skill_data = {
            "title": "Python Programming",
            "description": "Learn Python programming from basics to advanced",
            "category": "Programming",
            "proficiency_level": "Advanced",
            "value": 500
        }
        response = requests.post(f"{API_BASE_URL}/skills/", json=skill_data, headers=headers)
        if response.status_code == 201:
            skill = response.json()
            print(f"SUCCESS: Skill created: {skill['title']} (ID: {skill['id']})")
        else:
            print(f"ERROR: Skill creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: Skill creation error: {e}")
    
    # Test 4: Get all skills (with owner relationship)
    print("\n4. Testing /skills/ endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/skills/", headers=headers)
        if response.status_code == 200:
            skills = response.json()
            print(f"SUCCESS: Found {len(skills)} skills")
            if skills:
                first_skill = skills[0]
                print(f"   First skill: {first_skill['title']}")
                if 'owner' in first_skill:
                    print(f"   Owner: {first_skill['owner'].get('username', 'Unknown')}")
                else:
                    print("   WARNING: Owner relationship missing!")
            else:
                print("   No skills found")
        else:
            print(f"ERROR: Get skills failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: Get skills error: {e}")
    
    # Test 5: Get my skills
    print("\n5. Testing /skills/my-skills endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/skills/my-skills", headers=headers)
        if response.status_code == 200:
            my_skills = response.json()
            print(f"SUCCESS: Found {len(my_skills)} of my skills")
            for skill in my_skills:
                print(f"   - {skill['title']} (Value: {skill.get('value', 0)})")
        else:
            print(f"ERROR: Get my skills failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: Get my skills error: {e}")
    
    # Test 6: Test notifications
    print("\n6. Testing notifications endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/notifications/", headers=headers)
        if response.status_code == 200:
            notifications = response.json()
            print(f"SUCCESS: Found {len(notifications)} notifications")
        else:
            print(f"ERROR: Get notifications failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: Get notifications error: {e}")
    
    print("\n=== Test Complete ===")
    print("\nNext Steps:")
    print("1. Open your browser and go to: http://localhost:8000/frontend/debug.html")
    print("2. Test the frontend JavaScript functions")
    print("3. Try logging in and accessing the skills pages")
    print("4. Check browser console for any JavaScript errors")

if __name__ == "__main__":
    test_endpoints()
