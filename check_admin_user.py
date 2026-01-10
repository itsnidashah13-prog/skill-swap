#!/usr/bin/env python3
"""
Check Admin User in Database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

print('Checking Admin User in Database...')
print('='*40)

db = SessionLocal()
try:
    # Check by username
    admin_user = db.query(User).filter(User.username == 'admin').first()
    if admin_user:
        print('Found admin user by username:')
        print(f'   Username: {admin_user.username}')
        print(f'   Email: {admin_user.email}')
        print(f'   Password Hash: {admin_user.password_hash[:50]}...')
        print(f'   Is Active: {admin_user.is_active}')
    else:
        print('Admin user NOT found by username')
    
    print()
    
    # Check by email
    admin_by_email = db.query(User).filter(User.email == 'admin@example.com').first()
    if admin_by_email:
        print('Found admin user by email:')
        print(f'   Username: {admin_by_email.username}')
        print(f'   Email: {admin_by_email.email}')
        print(f'   Password Hash: {admin_by_email.password_hash[:50]}...')
        print(f'   Is Active: {admin_by_email.is_active}')
    else:
        print('Admin user NOT found by email')
        
    print()
    print('All users with admin in name/email:')
    admin_like_users = db.query(User).filter(
        (User.username.like('%admin%')) | (User.email.like('%admin%'))
    ).all()
    
    if admin_like_users:
        for user in admin_like_users:
            print(f'   {user.username} - {user.email}')
    else:
        print('No users found with admin in username/email')

finally:
    db.close()
