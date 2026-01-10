#!/usr/bin/env python3
"""
Real-time Terminal Monitor for Skill Exchange Debugging
"""

import subprocess
import time
import requests
import threading
import sys
import os

def monitor_backend_realtime():
    """Monitor backend in real-time and trigger requests"""
    print("REAL-TIME BACKEND TERMINAL MONITOR")
    print("="*60)
    
    # Check if backend is already running
    try:
        response = requests.get('http://127.0.0.1:8000/health', timeout=2)
        if response.ok:
            print("Backend is already running!")
            print("Monitoring existing backend process...")
            monitor_existing_backend()
        else:
            print("Backend not responding properly")
            print("Starting new backend process...")
            start_and_monitor_backend()
    except:
        print("Backend not running")
        print("Starting new backend process...")
        start_and_monitor_backend()

def monitor_existing_backend():
    """Monitor existing backend and test requests"""
    print("\n" + "="*60)
    print("TESTING EXISTING BACKEND - WATCH YOUR TERMINAL!")
    print("="*60)
    
    # Test various scenarios to trigger different errors
    test_scenarios = [
        {
            "name": "No Authorization Header",
            "headers": {},
            "data": {"skill_id": 10, "message": "Test message"},
            "expected_debug": [
                "DEBUG: Received skill exchange request",
                "ERROR: Invalid authorization header"
            ]
        },
        {
            "name": "Invalid Token",
            "headers": {"Authorization": "Bearer invalid_token_12345"},
            "data": {"skill_id": 10, "message": "Test message"},
            "expected_debug": [
                "DEBUG: Received skill exchange request",
                "DEBUG: Authorization header: Bearer invalid_token_12345",
                "DEBUG: Extracted token: invalid_token_12345...",
                "ERROR: Invalid token"
            ]
        },
        {
            "name": "Malformed JWT Token",
            "headers": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid.signature"},
            "data": {"skill_id": 10, "message": "Test message"},
            "expected_debug": [
                "DEBUG: Received skill exchange request",
                "DEBUG: Authorization header: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid.signature",
                "DEBUG: Extracted token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid.signature...",
                "ERROR: Invalid token"
            ]
        },
        {
            "name": "Valid Format Token (but fake)",
            "headers": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciJ9.fake_signature"},
            "data": {"skill_id": 10, "message": "Test message"},
            "expected_debug": [
                "DEBUG: Received skill exchange request",
                "DEBUG: Authorization header: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciJ9.fake_signature",
                "DEBUG: Extracted token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciJ9.fake_signature...",
                "DEBUG: Decoded username: testuser",
                "ERROR: User not found in database: testuser"
            ]
        }
    ]
    
    print("\nTESTING DIFFERENT ERROR SCENARIOS:")
    print("Watch your backend terminal for these specific debug messages...")
    print("-" * 60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nTest {i}: {scenario['name']}")
        print("-" * 40)
        print("Expected in terminal:")
        for debug_msg in scenario['expected_debug']:
            print(f"  - {debug_msg}")
        
        print(f"\nSending request...")
        try:
            response = requests.post(
                'http://127.0.0.1:8000/request-skill',
                json=scenario['data'],
                headers=scenario['headers'],
                timeout=5
            )
            print(f"Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
        
        print("\nCheck your backend terminal now...")
        input("Press Enter to continue to next test...")
    
    print("\n" + "="*60)
    print("NOW TEST WITH YOUR FRONTEND!")
    print("="*60)
    
    print("\nFRONTEND TESTING INSTRUCTIONS:")
    print("1. Open your browser and go to: http://127.0.0.1:3000/frontend/index.html")
    print("2. Login with your credentials")
    print("3. Go to 'Browse Skills' page")
    print("4. Click 'Request Exchange' on any skill")
    print("5. Fill in the message")
    print("6. Click 'Send Request'")
    print("7. IMMEDIATELY look at your backend terminal")
    
    print("\nWHAT TO LOOK FOR IN TERMINAL:")
    print("-" * 40)
    print("SUCCESS PATH (if working):")
    print("  DEBUG: Received skill exchange request")
    print("  DEBUG: Authorization header: Bearer <token>")
    print("  DEBUG: Extracted token: <token>...")
    print("  DEBUG: Decoded username: <username>")
    print("  DEBUG: Found user: <username> (ID: <id>)")
    print("  DEBUG: Request data - skill_id: <id>, message: '<message>'")
    print("  DEBUG: Found skill: <title> (ID: <id>, Owner: <id>)")
    print("  DEBUG: Creating exchange request...")
    print("  DEBUG: Exchange request created with ID: <id>")
    print("  DEBUG: Creating notification for skill owner...")
    print("  DEBUG: Notification created successfully")
    print("  DEBUG: Preparing response...")
    print("  DEBUG: Skill owner username: <username>")
    
    print("\nERROR PATH (if failing):")
    print("  Look for any of these:")
    print("  - ERROR: Invalid authorization header")
    print("  - ERROR: Invalid token: <specific error>")
    print("  - ERROR: Token has expired")
    print("  - ERROR: User not found in database: <username>")
    print("  - ERROR: Skill not found: <skill_id>")
    print("  - ERROR: User requesting own skill")
    print("  - ERROR: Failed to create skill exchange request")
    print("  - ERROR: Notification creation failed")
    print("  - ERROR: Unexpected error in direct_request_skill")
    
    print("\nCRITICAL - LOOK FOR TRACEBACK:")
    print("  Traceback (most recent call last):")
    print("    File \"main.py\", line <number>, in direct_request_skill")
    print("      <problematic code line>")
    print("  <ExceptionType>: <error message>")
    
    print("\nCOPY THE COMPLETE TERMINAL OUTPUT:")
    print("  1. Select all text in your terminal")
    print("  2. Copy (Ctrl+C)")
    print("  3. Paste here for analysis")
    
    input("\nReady! Press Enter when you've tested the frontend...")

def start_and_monitor_backend():
    """Start new backend and monitor"""
    print("Starting new backend process...")
    # This would start a new backend but we'll focus on monitoring existing one
    print("Please start backend manually: python main.py")
    print("Then run this script again to monitor")

def analyze_terminal_output():
    """Analyze what terminal output means"""
    print("\n" + "="*60)
    print("TERMINAL OUTPUT ANALYSIS GUIDE")
    print("="*60)
    
    print("\n📊 COMMON ERROR PATTERNS AND SOLUTIONS:")
    print("-" * 50)
    
    patterns = [
        {
            "pattern": "AttributeError: 'Skill' object has no attribute 'user'",
            "cause": "Skill-User relationship not loaded",
            "solution": "Add joinedload(Skill.owner) in get_skill function"
        },
        {
            "pattern": "jwt.exceptions.InvalidTokenError",
            "cause": "JWT token is malformed or invalid",
            "solution": "Check token format and secret key"
        },
        {
            "pattern": "User not found in database",
            "cause": "Token decoded but user doesn't exist",
            "solution": "Check user registration and database"
        },
        {
            "pattern": "Skill not found",
            "cause": "Skill ID doesn't exist in database",
            "solution": "Verify skill exists and is active"
        },
        {
            "pattern": "sqlalchemy.exc.IntegrityError",
            "cause": "Database constraint violation",
            "solution": "Check foreign keys and required fields"
        },
        {
            "pattern": "Cannot request your own skill",
            "cause": "User trying to request their own skill",
            "solution": "This is validation - choose different skill"
        }
    ]
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\n{i}. {pattern['pattern']}")
        print(f"   Cause: {pattern['cause']}")
        print(f"   Solution: {pattern['solution']}")
    
    print("\n" + "="*60)
    print("DEBUGGING COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    monitor_backend_realtime()
    analyze_terminal_output()
