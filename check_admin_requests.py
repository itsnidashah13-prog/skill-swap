#!/usr/bin/env python3
"""
Check Admin Exchange Requests
"""

from database import SessionLocal
from crud import get_skill_exchange_requests

def check_admin_requests():
    """Check if admin user has any exchange requests"""
    
    print('Checking Admin Exchange Requests...')
    print('='*40)
    
    try:
        # Create database session
        db = SessionLocal()
        
        print('Getting all exchange requests...')
        
        # Get all requests
        all_requests = get_skill_exchange_requests(db, skip=0, limit=100)
        
        print(f'Total requests in database: {len(all_requests)}')
        
        if all_requests:
            print('Sample requests:')
            for i, req in enumerate(all_requests[:5]):
                print(f'  {i+1}. ID: {req.get("id")}, Requester: {req.get("requester", {}).get("username")}, Owner: {req.get("skill_owner", {}).get("username")}, Status: {req.get("status")}')
        
        # Check for admin user (ID 40)
        admin_requests = [req for req in all_requests if req.get('requester_id') == 40 or req.get('skill_owner_id') == 40]
        print(f'Requests involving admin user (ID 40): {len(admin_requests)}')
        
        if admin_requests:
            print('Admin requests:')
            for i, req in enumerate(admin_requests):
                print(f'  {i+1}. ID: {req.get("id")}, Requester: {req.get("requester", {}).get("username")}, Owner: {req.get("skill_owner", {}).get("username")}, Status: {req.get("status")}')
        
        db.close()
        print('SUCCESS: Admin requests check complete')
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_admin_requests()
