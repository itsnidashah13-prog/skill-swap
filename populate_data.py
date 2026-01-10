#!/usr/bin/env python3
"""
Script to populate the database with default users and skills
"""

import sys
import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import engine, Base, SessionLocal
from models import User, Skill

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_default_data():
    """Create default users and skills in the database"""
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping data creation.")
            return
        
        print("Creating default users and skills...")
        
        # Create default users
        default_users = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "bio": "Experienced software developer with 5+ years in web development",
                "password": "password123"
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com",
                "full_name": "Jane Smith",
                "bio": "Creative graphic designer specializing in branding and UI/UX",
                "password": "password123"
            },
            {
                "username": "mike_wilson",
                "email": "mike@example.com",
                "full_name": "Mike Wilson",
                "bio": "Digital marketing expert with focus on social media and content strategy",
                "password": "password123"
            },
            {
                "username": "sarah_chen",
                "email": "sarah@example.com",
                "full_name": "Sarah Chen",
                "bio": "Data scientist and machine learning engineer",
                "password": "password123"
            }
        ]
        
        created_users = []
        for user_data in default_users:
            hashed_password = pwd_context.hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                bio=user_data["bio"],
                password_hash=hashed_password
            )
            db.add(user)
            created_users.append(user)
        
        db.commit()
        print(f"Created {len(created_users)} default users")
        
        # Create default skills
        default_skills = [
            # John Doe - Technical Skills
            {
                "user_id": created_users[0].id,
                "title": "Python Programming",
                "description": "Expert in Python development, including Django, Flask, and data analysis libraries. Can help with web development, automation scripts, and data science projects.",
                "category": "Programming",
                "proficiency_level": "Expert"
            },
            {
                "user_id": created_users[0].id,
                "title": "Web Development",
                "description": "Full-stack web development with HTML, CSS, JavaScript, React, and Node.js. Can build complete web applications from scratch.",
                "category": "Web Development",
                "proficiency_level": "Advanced"
            },
            {
                "user_id": created_users[0].id,
                "title": "Database Design",
                "description": "Experienced in SQL and NoSQL database design, optimization, and management. Works with PostgreSQL, MySQL, MongoDB.",
                "category": "Database",
                "proficiency_level": "Advanced"
            },
            
            # Jane Smith - Design Skills
            {
                "user_id": created_users[1].id,
                "title": "Graphic Design",
                "description": "Professional graphic designer with expertise in Adobe Creative Suite. Can create logos, branding materials, marketing collateral, and digital artwork.",
                "category": "Design",
                "proficiency_level": "Expert"
            },
            {
                "user_id": created_users[1].id,
                "title": "UI/UX Design",
                "description": "User interface and user experience design for web and mobile applications. Focus on creating intuitive, user-friendly designs.",
                "category": "Design",
                "proficiency_level": "Advanced"
            },
            {
                "user_id": created_users[1].id,
                "title": "Logo Design",
                "description": "Custom logo design for businesses and brands. Can create unique, memorable logos that represent your brand identity.",
                "category": "Design",
                "proficiency_level": "Expert"
            },
            
            # Mike Wilson - Marketing Skills
            {
                "user_id": created_users[2].id,
                "title": "Digital Marketing",
                "description": "Comprehensive digital marketing strategies including SEO, SEM, social media marketing, and email campaigns. Can help grow your online presence.",
                "category": "Marketing",
                "proficiency_level": "Advanced"
            },
            {
                "user_id": created_users[2].id,
                "title": "Social Media Management",
                "description": "Expert in managing social media accounts across all platforms. Content creation, scheduling, engagement strategies, and analytics.",
                "category": "Marketing",
                "proficiency_level": "Expert"
            },
            {
                "user_id": created_users[2].id,
                "title": "Content Marketing",
                "description": "Content strategy and creation for blogs, websites, and social media. Can help with content planning, writing, and distribution.",
                "category": "Marketing",
                "proficiency_level": "Advanced"
            },
            
            # Sarah Chen - Data Science Skills
            {
                "user_id": created_users[3].id,
                "title": "Data Science",
                "description": "Data analysis, machine learning, and statistical modeling. Can help with data-driven insights, predictive models, and data visualization.",
                "category": "Data Science",
                "proficiency_level": "Expert"
            },
            {
                "user_id": created_users[3].id,
                "title": "Machine Learning",
                "description": "Machine learning engineer with experience in TensorFlow, PyTorch, and scikit-learn. Can build and deploy ML models.",
                "category": "Data Science",
                "proficiency_level": "Advanced"
            },
            {
                "user_id": created_users[3].id,
                "title": "Data Visualization",
                "description": "Create compelling data visualizations and dashboards using tools like Tableau, Power BI, and Python libraries.",
                "category": "Data Science",
                "proficiency_level": "Intermediate"
            }
        ]
        
        for skill_data in default_skills:
            skill = Skill(**skill_data)
            db.add(skill)
        
        db.commit()
        print(f"Created {len(default_skills)} default skills")
        
        # Verify data was created
        user_count = db.query(User).count()
        skill_count = db.query(Skill).count()
        
        print(f"\n✅ Database populated successfully!")
        print(f"📊 Total Users: {user_count}")
        print(f"🔧 Total Skills: {skill_count}")
        
        print(f"\n🔑 Default Login Credentials:")
        print(f"Username: john_doe, Password: password123")
        print(f"Username: jane_smith, Password: password123")
        print(f"Username: mike_wilson, Password: password123")
        print(f"Username: sarah_chen, Password: password123")
        
    except Exception as e:
        print(f"❌ Error creating data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_default_data()
