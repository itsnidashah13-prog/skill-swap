#!/usr/bin/env python3
"""
Check and Create Admin User in Database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import User
from crud import hash_password

def check_admin_user():
    """Check if admin user exists and create if not"""
    
    print("Checking Database for Admin User...")
    print("="*50)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            print("Admin user already exists:")
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   Full Name: {admin_user.full_name}")
            print(f"   Is Active: {admin_user.is_active}")
            print(f"   Created: {admin_user.created_at}")
            return True
        else:
            print("Admin user not found in database")
            print("Creating default admin user...")
            
            # Create admin user
            admin_data = {
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "System Administrator",
                "password": "admin123",
                "bio": "Default admin user for skill exchange platform",
                "is_active": True
            }
            
            # Hash the password
            hashed_password = hash_password(admin_data["password"])
            
            # Create user object
            new_admin = User(
                username=admin_data["username"],
                email=admin_data["email"],
                full_name=admin_data["full_name"],
                password_hash=hashed_password,
                bio=admin_data["bio"],
                is_active=admin_data["is_active"]
            )
            
            # Add to database
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            
            print("Admin user created successfully:")
            print(f"   Username: {new_admin.username}")
            print(f"   Email: {new_admin.email}")
            print(f"   Full Name: {new_admin.full_name}")
            print(f"   Is Active: {new_admin.is_active}")
            print(f"   User ID: {new_admin.id}")
            print(f"   Created: {new_admin.created_at}")
            print()
            print("IMPORTANT: Change the default password in production!")
            
            return True
            
    except Exception as e:
        print(f"Error checking/creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def check_all_users():
    """Check all users in database"""
    
    print("\nAll Users in Database:")
    print("="*30)
    
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        if not users:
            print("No users found in database")
            return
        
        for user in users:
            role = "Admin" if user.username == "admin" else "User"
            print(f"   {user.username} ({role}) - {user.email} - Active: {user.is_active}")
            
    except Exception as e:
        print(f"Error listing users: {e}")
    finally:
        db.close()

def check_database_connection():
    """Test database connection"""
    
    print("Testing Database Connection...")
    print("="*30)
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            print(f"Database connected successfully")
            print(f"   Total users: {user_count}")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def main():
    """Main function"""
    
    print("Skill Exchange - Admin User Setup")
    print("="*50)
    
    # Check database connection
    if not check_database_connection():
        print("Cannot proceed without database connection")
        return
    
    # Check all users
    check_all_users()
    
    # Check and create admin user
    admin_created = check_admin_user()
    
    if admin_created:
        print("\nAdmin user setup completed!")
        print("You can now login to admin dashboard with:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\nAdmin Dashboard URL:")
        print("   http://127.0.0.1:3005/admin_final.html")
        print("\nBackend Admin Login:")
        print("   POST http://127.0.0.1:8000/admin/login")
    else:
        print("\nAdmin user setup failed!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
