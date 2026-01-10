#!/usr/bin/env python3
"""
Check database connection and skill records
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Skill, User

# Database connection
DATABASE_URL = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=skill_swap;Trusted_Connection=yes"

def check_database():
    print("DATABASE DEBUG CHECK")
    print("=" * 50)
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        print("Database connection successful")
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if tables exist
        print("\nTABLE CHECK:")
        try:
            # Check skills table
            skills_count = db.execute(text("SELECT COUNT(*) FROM skills")).scalar()
            print(f"Skills table exists, records: {skills_count}")
        except Exception as e:
            print(f"Skills table error: {e}")
            
        try:
            # Check users table
            users_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
            print(f"Users table exists, records: {users_count}")
        except Exception as e:
            print(f"Users table error: {e}")
        
        # Check actual skill data
        print("\nSKILL DATA CHECK:")
        try:
            skills = db.query(Skill).all()
            print(f"Found {len(skills)} skills in database")
            
            if skills:
                print("\nFirst 3 skills:")
                for i, skill in enumerate(skills[:3]):
                    print(f"  {i+1}. ID: {skill.id}, Title: {skill.title}, Active: {skill.is_active}")
                    print(f"     User ID: {skill.user_id}, Category: {skill.category}")
            else:
                print("No skills found in database!")
                
                # Check if there are any users
                users = db.query(User).all()
                print(f"Found {len(users)} users in database")
                
                if users:
                    print("Available users:")
                    for user in users[:3]:
                        print(f"  - ID: {user.id}, Username: {user.username}")
                        
        except Exception as e:
            print(f"Error querying skills: {e}")
        
        # Test the exact query that get_skills() uses
        print("\nTESTING CRUD QUERY:")
        try:
            from crud import get_skills
            skills_from_crud = get_skills(db)
            print(f"get_skills() returned: {len(skills_from_crud)} skills")
            
            if skills_from_crud:
                first_skill = skills_from_crud[0]
                print(f"   First skill: {first_skill.title}")
                print(f"   Has owner: {hasattr(first_skill, 'owner')}")
                if hasattr(first_skill, 'owner') and first_skill.owner:
                    print(f"   Owner: {first_skill.owner.username}")
                else:
                    print("   Owner relationship not loaded!")
        except Exception as e:
            print(f"Error in get_skills(): {e}")
            import traceback
            traceback.print_exc()
        
        db.close()
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
