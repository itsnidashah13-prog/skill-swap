#!/usr/bin/env python3
"""
Test CRUD Function Directly
"""

from database import SessionLocal
from crud import update_skill_exchange_request_status

def test_crud_function_direct():
    """Test CRUD function directly"""
    
    print('Testing CRUD Function Directly...')
    print('='*50)
    
    try:
        # Create database session
        db = SessionLocal()
        
        print('Testing update_skill_exchange_request_status...')
        
        # Test the function with request ID 1
        result = update_skill_exchange_request_status(db, request_id=1, status='Accepted')
        
        print(f'Function returned: {type(result)}')
        print(f'Result: {result}')
        
        if result:
            print(f'SUCCESS: Request updated to status: {result.status}')
        else:
            print('ERROR: Function returned None')
        
        db.close()
        print('SUCCESS: CRUD function test complete')
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crud_function_direct()
