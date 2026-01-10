#!/usr/bin/env python3
"""
Test User CRUD Function
"""

from database import get_db, SessionLocal
from crud import get_skill_exchange_requests_for_user

def test_user_crud():
    """Test user CRUD function directly"""
    
    print('Testing User CRUD Function...')
    print('='*40)
    
    try:
        # Create database session
        db = SessionLocal()
        
        print('Testing get_skill_exchange_requests_for_user...')
        
        # Test with user ID 40 (admin user)
        requests = get_skill_exchange_requests_for_user(db, user_id=40, skip=0, limit=100)
        
        print(f'Function returned: {type(requests)}')
        print(f'Number of requests: {len(requests) if requests else 0}')
        
        if requests:
            print('First request structure:')
            first_request = requests[0]
            print(f'  Type: {type(first_request)}')
            print(f'  Class: {first_request.__class__.__name__}')
            if hasattr(first_request, '__dict__'):
                print(f'  Attributes: {list(first_request.__dict__.keys())}')
        
        db.close()
        print('SUCCESS: User CRUD function working')
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_crud()
