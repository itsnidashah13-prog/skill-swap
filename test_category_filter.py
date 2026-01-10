#!/usr/bin/env python3
"""
Test Category Filter Functionality
"""

import requests
import json

def test_category_filter():
    """Test if category filter is working properly"""
    
    base_url = 'http://127.0.0.1:8001'
    
    print('Testing Category Filter Functionality...')
    print('='*50)
    
    # Test 1: Get all skills (no filter)
    print('1. Testing all skills (no filter)...')
    try:
        response = requests.get(f'{base_url}/api/skills/', timeout=10)
        
        if response.ok:
            all_skills = response.json()
            print(f'   SUCCESS: {len(all_skills)} skills found')
            
            # Show categories
            categories = set()
            for skill in all_skills:
                categories.add(skill.get('category', 'Unknown'))
            print(f'   Available categories: {sorted(list(categories))}')
            
        else:
            print(f'   ERROR: Failed to get skills (Status: {response.status_code})')
            return
            
    except Exception as e:
        print(f'   ERROR: {e}')
        return
    
    print()
    
    # Test 2: Filter by specific categories
    test_categories = ['Programming', 'Design', 'Music', 'Language', 'Cooking', 'Sports', 'Other']
    
    for category in test_categories:
        print(f'2. Testing category filter: {category}')
        try:
            response = requests.get(f'{base_url}/api/skills/?category={category}', timeout=10)
            
            if response.ok:
                filtered_skills = response.json()
                print(f'   SUCCESS: {len(filtered_skills)} skills found in {category}')
                
                # Verify all results are in the correct category
                for skill in filtered_skills:
                    if skill.get('category') != category:
                        print(f'   ERROR: Skill "{skill.get("title")}" is in category "{skill.get("category")}" not "{category}"')
                        break
                else:
                    print(f'   SUCCESS: All skills correctly filtered by {category}')
                    
            else:
                print(f'   ERROR: Failed to filter by {category} (Status: {response.status_code})')
                
        except Exception as e:
            print(f'   ERROR: {e}')
        
        print()
    
    # Test 3: Test frontend filter functionality
    print('3. Testing frontend filter URL generation...')
    try:
        # Simulate frontend filter logic
        category = 'Programming'
        endpoint = 'skills/'
        if category:
            endpoint += f'?category={category}'
        
        expected_url = f'{base_url}/api/{endpoint}'
        print(f'   Expected URL: {expected_url}')
        
        response = requests.get(expected_url, timeout=10)
        
        if response.ok:
            filtered_skills = response.json()
            print(f'   SUCCESS: Frontend URL works, {len(filtered_skills)} skills found')
        else:
            print(f'   ERROR: Frontend URL failed (Status: {response.status_code})')
            
    except Exception as e:
        print(f'   ERROR: {e}')
    
    print()
    
    # Test 4: Test invalid category
    print('4. Testing invalid category...')
    try:
        response = requests.get(f'{base_url}/api/skills/?category=InvalidCategory', timeout=10)
        
        if response.ok:
            filtered_skills = response.json()
            print(f'   SUCCESS: Invalid category handled gracefully, {len(filtered_skills)} skills found')
        else:
            print(f'   ERROR: Invalid category caused error (Status: {response.status_code})')
            
    except Exception as e:
        print(f'   ERROR: {e}')
    
    print()
    print('Category Filter Testing Complete!')

if __name__ == "__main__":
    test_category_filter()
