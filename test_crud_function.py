#!/usr/bin/env python3
"""
Test CRUD Function Directly
"""

from database import get_db, SessionLocal
from crud import get_skill_exchange_requests

def test_crud_function():
    """Test CRUD function directly"""
    
    print('Testing CRUD Function Directly...')
    print('='*40)
    
    try:
        # Create database session
        db = SessionLocal()
        
        print('Testing get_skill_exchange_requests...')
        
        # Test the function
        requests = get_skill_exchange_requests(db, skip=0, limit=100)
        
        print(f'Function returned: {type(requests)}')
        print(f'Number of requests: {len(requests) if requests else 0}')
        
        if requests:
            print('First request structure:')
            first_request = requests[0]
            print(f'  Type: {type(first_request)}')
            print(f'  Keys: {list(first_request.keys()) if isinstance(first_request, dict) else "Not a dict"}')
            
            if isinstance(first_request, dict):
                for key, value in first_request.items():
                    print(f'  {key}: {type(value)} = {str(value)[:50]}...')
        
        db.close()
        print('SUCCESS: CRUD function working')
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crud_function()
