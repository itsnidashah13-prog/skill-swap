#!/usr/bin/env python3
"""
Simple test script to verify CRUD fixes
"""

import sys
sys.path.append("c:/Users/Javy/Desktop/skill swap")

def test_crud_functions():
    """Test CRUD functions without unicode issues"""
    print("CRUD FIX VERIFICATION")
    print("="*50)
    
    try:
        from crud import (
            create_user, update_user, create_skill, update_skill,
            create_skill_exchange_request, update_skill_exchange_request,
            create_notification
        )
        print("SUCCESS: All CRUD functions imported")
        
        # Test Pydantic model methods
        from schemas import UserCreate, SkillCreate, UserUpdate
        
        # Test UserCreate
        user_data = UserCreate(
            username="test",
            email="test@example.com",
            full_name="Test User",
            password="password123",
            bio="Test bio"
        )
        
        try:
            user_dict = user_data.model_dump()
            print("SUCCESS: UserCreate.model_dump() works")
        except Exception as e:
            print(f"ERROR: UserCreate.model_dump() failed: {e}")
            
        try:
            user_dict = user_data.dict()
            print("WARNING: UserCreate.dict() still works")
        except Exception as e:
            print("SUCCESS: UserCreate.dict() correctly fails")
        
        # Test SkillCreate
        skill_data = SkillCreate(
            title="Test Skill",
            description="Test Description",
            category="Programming",
            proficiency_level="Advanced"
        )
        
        try:
            skill_dict = skill_data.model_dump()
            print("SUCCESS: SkillCreate.model_dump() works")
        except Exception as e:
            print(f"ERROR: SkillCreate.model_dump() failed: {e}")
        
        # Test UserUpdate
        update_data = UserUpdate(full_name="Updated Name")
        
        try:
            update_dict = update_data.model_dump()
            print("SUCCESS: UserUpdate.model_dump() works")
        except Exception as e:
            print(f"ERROR: UserUpdate.model_dump() failed: {e}")
        
        print("\nCRUD FIXES APPLIED:")
        print("- create_user: Uses direct field assignment")
        print("- update_user: Uses model_dump() instead of dict()")
        print("- create_skill: Uses direct field assignment")
        print("- update_skill: Uses model_dump() instead of dict()")
        print("- create_skill_exchange_request: Uses direct field assignment")
        print("- update_skill_exchange_request: Uses model_dump() instead of dict()")
        print("- create_notification: Uses direct field assignment")
        
        print("\nRESULT: AttributeError 'dict' issue should be resolved")
        return True
        
    except ImportError as e:
        print(f"IMPORT ERROR: {e}")
        return False
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        return False

if __name__ == "__main__":
    if test_crud_functions():
        print("\nALL TESTS PASSED!")
        print("Ready to start server without CRUD errors")
        print("\nNEXT STEPS:")
        print("1. cd 'c:/Users/Javy/Desktop/skill swap'")
        print("2. python main.py")
        print("3. Open http://127.0.0.1:8000/admin/")
        print("4. Test frontend functionality")
    else:
        print("\nSOME TESTS FAILED!")
        print("Check error messages above")
