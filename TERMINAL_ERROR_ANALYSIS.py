#!/usr/bin/env python3
"""
Terminal Error Analysis - What you should see in backend logs
"""

import requests
import json

def analyze_terminal_errors():
    """Analyze what errors should appear in terminal"""
    print("TERMINAL ERROR ANALYSIS")
    print("="*60)
    
    print("WHEN YOU CLICK 'SEND REQUEST' IN FRONTEND:")
    print("-" * 50)
    
    print("EXPECTED BACKEND TERMINAL OUTPUT:")
    print("DEBUG: Received skill exchange request")
    print("DEBUG: Authorization header: Bearer <token>")
    print("DEBUG: Extracted token: <token>...")
    
    print("\nIF TOKEN IS INVALID/EXPIRED:")
    print("ERROR: Invalid token: <error details>")
    print("OR")
    print("ERROR: Token has expired")
    
    print("\nIF USER NOT FOUND:")
    print("ERROR: User not found in database: <username>")
    
    print("\nIF SKILL NOT FOUND:")
    print("ERROR: Skill not found: <skill_id>")
    
    print("\nIF REQUESTING OWN SKILL:")
    print("ERROR: User requesting own skill: <user_id> == <user_id>")
    
    print("\nIF DATABASE ERROR:")
    print("ERROR: Failed to create skill exchange request: <error>")
    print("ERROR: Exception type: <type>")
    print("ERROR: Exception details: <details>")
    
    print("\nIF NOTIFICATION ERROR:")
    print("ERROR: Notification creation failed: <error>")
    print("WARNING: Continuing without notification...")
    
    print("\n" + "="*60)
    print("COMMON PYTHON TRACEBACK PATTERNS:")
    print("="*60)
    
    print("1. IMPORT ERROR:")
    print("   Traceback (most recent call last):")
    print("   File \"main.py\", line X, in <module>")
    print("     import some_module")
    print("   ModuleNotFoundError: No module named 'some_module'")
    
    print("\n2. ATTRIBUTE ERROR:")
    print("   Traceback (most recent call last):")
    print("   File \"main.py\", line X, in direct_request_skill")
    print("     skill.user.username")
    print("   AttributeError: 'Skill' object has no attribute 'user'")
    
    print("\n3. DATABASE ERROR:")
    print("   Traceback (most recent call last):")
    print("   File \"main.py\", line X, in direct_request_skill")
    print("     db.add(db_request)")
    print("   sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed")
    
    print("\n4. JWT ERROR:")
    print("   Traceback (most recent call last):")
    print("   File \"main.py\", line X, in direct_request_skill")
    print("     payload = jwt.decode(token, ...)")
    print("   jwt.exceptions.InvalidTokenError: Not enough segments")
    
    print("\n5. TYPE ERROR:")
    print("   Traceback (most recent call last):")
    print("   File \"main.py\", line X, in direct_request_skill")
    print("     skill_id = request.skill_id")
    print("   TypeError: 'NoneType' object is not subscriptable")
    
    print("\n" + "="*60)
    print("WHAT TO CHECK IN YOUR TERMINAL:")
    print("="*60)
    
    print("1. LOOK FOR 'Traceback (most recent call last):'")
    print("   - This indicates a Python exception")
    print("   - Shows exact file and line number")
    print("   - Most important for debugging")
    
    print("\n2. LOOK FOR 'ERROR:' PREFIX")
    print("   - These are our custom debug messages")
    print("   - Show specific validation failures")
    print("   - Easier to understand than traceback")
    
    print("\n3. LOOK FOR 'DEBUG:' PREFIX")
    print("   - These show successful execution steps")
    print("   - Help track where the process stops")
    print("   - Useful for identifying bottlenecks")
    
    print("\n4. LOOK FOR 'WARNING:' PREFIX")
    print("   - Non-critical issues")
    print("   - Process continues but with problems")
    print("   - Usually notification failures")
    
    print("\n" + "="*60)
    print("TESTING LIVE REQUESTS:")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test different scenarios
    test_cases = [
        {
            "name": "No Authorization",
            "headers": {},
            "expected": "Authorization header required with Bearer token"
        },
        {
            "name": "Invalid Token",
            "headers": {"Authorization": "Bearer invalid_token"},
            "expected": "Invalid token"
        },
        {
            "name": "Malformed JWT",
            "headers": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid"},
            "expected": "Invalid token"
        },
        {
            "name": "Empty Skill ID",
            "headers": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test.signature"},
            "data": {"skill_id": None, "message": "test"},
            "expected": "Skill ID is required"
        },
        {
            "name": "Empty Message",
            "headers": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test.signature"},
            "data": {"skill_id": 1, "message": ""},
            "expected": "Message is required"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 30)
        
        try:
            data = test.get('data', {"skill_id": 1, "message": "test"})
            response = requests.post(
                f"{base_url}/request-skill",
                json=data,
                headers=test['headers'],
                timeout=5
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if test['expected'] in response.text:
                print(f"✅ Expected error found: {test['expected']}")
            else:
                print(f"❌ Expected error not found. Expected: {test['expected']}")
                
        except Exception as e:
            print(f"Request failed: {e}")
    
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    
    print("1. START YOUR BACKEND:")
    print("   cd \"c:/Users/Javy/Desktop/skill swap\"")
    print("   python main.py")
    
    print("\n2. WATCH THE TERMINAL:")
    print("   - Keep the terminal window visible")
    print("   - Look for DEBUG and ERROR messages")
    print("   - Note any Traceback output")
    
    print("\n3. TEST IN FRONTEND:")
    print("   - Open http://127.0.0.1:3000/frontend/index.html")
    print("   - Login with valid credentials")
    print("   - Go to Browse Skills")
    print("   - Click 'Request Exchange'")
    print("   - Fill message and click 'Send Request'")
    
    print("\n4. ANALYZE TERMINAL OUTPUT:")
    print("   - Look for 'Traceback (most recent call last):'")
    print("   - Check for 'ERROR:' messages")
    print("   - Note the exact line number")
    print("   - Copy the complete error message")
    
    print("\n5. SHARE THE ERROR:")
    print("   - Copy the complete terminal output")
    print("   - Include the Traceback if present")
    print("   - Note the specific error message")
    print("   - Mention what action triggered it")
    
    print("\n" + "="*60)
    print("READY TO ANALYZE TERMINAL ERRORS!")
    print("="*60)

if __name__ == "__main__":
    analyze_terminal_errors()
