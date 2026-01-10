#!/usr/bin/env python3
"""
Test Frontend UI Loading
"""

import requests
import json

def test_frontend_ui():
    """Test if frontend UI is loading properly"""
    
    base_url = 'http://127.0.0.1:3002'
    
    print('Testing Frontend UI Loading...')
    print('='*50)
    
    # Test 1: Check if index.html loads
    print('1. Testing index.html loading...')
    try:
        response = requests.get(base_url + '/frontend/index.html', timeout=10)
        
        if response.ok:
            print(f'   SUCCESS: index.html loaded (Status: {response.status_code})')
            print(f'   Content length: {len(response.text)} characters')
            
            # Check for key elements
            if 'Skill Swap' in response.text:
                print('   ✓ Title found')
            else:
                print('   ✗ Title not found')
                
            if 'style_fixed.css' in response.text:
                print('   ✓ CSS file linked')
            else:
                print('   ✗ CSS file not linked')
                
            if 'script.js' in response.text:
                print('   ✓ JavaScript file linked')
            else:
                print('   ✗ JavaScript file not linked')
                
        else:
            print(f'   ERROR: Failed to load index.html (Status: {response.status_code})')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 2: Check if CSS loads
    print('2. Testing CSS loading...')
    try:
        response = requests.get(base_url + '/frontend/style_fixed.css', timeout=10)
        
        if response.ok:
            print(f'   SUCCESS: CSS loaded (Status: {response.status_code})')
            print(f'   Content length: {len(response.text)} characters')
            
            # Check for key CSS classes
            if '.page-section' in response.text:
                print('   ✓ Page sections CSS found')
            else:
                print('   ✗ Page sections CSS not found')
                
        else:
            print(f'   ERROR: Failed to load CSS (Status: {response.status_code})')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 3: Check if JavaScript loads
    print('3. Testing JavaScript loading...')
    try:
        response = requests.get(base_url + '/frontend/script.js', timeout=10)
        
        if response.ok:
            print(f'   SUCCESS: JavaScript loaded (Status: {response.status_code})')
            print(f'   Content length: {len(response.text)} characters')
            
            # Check for key functions
            if 'showPage' in response.text:
                print('   ✓ showPage function found')
            else:
                print('   ✗ showPage function not found')
                
            if 'loadSkills' in response.text:
                print('   ✓ loadSkills function found')
            else:
                print('   ✗ loadSkills function not found')
                
        else:
            print(f'   ERROR: Failed to load JavaScript (Status: {response.status_code})')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    
    # Test 4: Check backend API connectivity
    print('4. Testing backend API connectivity...')
    try:
        response = requests.get('http://127.0.0.1:8001/api/skills/', timeout=10)
        
        if response.ok:
            print(f'   SUCCESS: Backend API reachable (Status: {response.status_code})')
            skills = response.json()
            print(f'   Skills available: {len(skills)}')
        else:
            print(f'   ERROR: Backend API not responding (Status: {response.status_code})')
            
    except Exception as e:
        print(f'   EXCEPTION: {e}')
    
    print()
    print('Frontend UI Testing Complete!')

if __name__ == "__main__":
    test_frontend_ui()
