#!/usr/bin/env python3
"""
Update Admin User Email to admin@example.com
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

def update_admin_email():
    """Update admin user email to admin@example.com"""
    
    print("Updating Admin User Email...")
    print("="*40)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Find admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            print(f"Found admin user:")
            print(f"   Username: {admin_user.username}")
            print(f"   Current Email: {admin_user.email}")
            print(f"   Full Name: {admin_user.full_name}")
            
            # Update email to admin@example.com
            admin_user.email = "admin@example.com"
            db.commit()
            db.refresh(admin_user)
            
            print(f"\nUpdated admin user email:")
            print(f"   New Email: {admin_user.email}")
            print(f"   Updated: {admin_user.created_at}")
            
            print(f"\nSUCCESS: Admin user email updated to admin@example.com")
            return True
            
        else:
            print("ERROR: Admin user not found in database")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to update admin email: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_admin_user():
    """Verify admin user details"""
    
    print("\nVerifying Admin User...")
    print("="*30)
    
    db = SessionLocal()
    
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            print(f"Admin User Details:")
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   Full Name: {admin_user.full_name}")
            print(f"   Is Active: {admin_user.is_active}")
            print(f"   User ID: {admin_user.id}")
            print(f"   Created: {admin_user.created_at}")
            
            if admin_user.email == "admin@example.com":
                print(f"\nVERIFIED: Admin email is correct (admin@example.com)")
                return True
            else:
                print(f"\nERROR: Admin email is incorrect ({admin_user.email})")
                return False
        else:
            print("ERROR: Admin user not found")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to verify admin user: {e}")
        return False
    finally:
        db.close()

def main():
    """Main function"""
    
    print("Skill Exchange - Admin Email Update")
    print("="*50)
    
    # Update admin email
    if update_admin_email():
        # Verify the update
        if verify_admin_user():
            print("\nAdmin user email update completed successfully!")
            print("Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@example.com")
            print("\nAdmin Dashboard URL:")
            print("   http://127.0.0.1:3005/admin_final.html")
        else:
            print("\nAdmin user email update failed verification!")
    else:
        print("\nAdmin user email update failed!")

if __name__ == "__main__":
    main()
