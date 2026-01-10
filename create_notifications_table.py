#!/usr/bin/env python3
"""
Script to create notifications table in the database
"""

from sqlalchemy import create_engine, text
from database import settings

def create_notifications_table():
    """Create notifications table if it doesn't exist"""
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as connection:
            # Check if table already exists
            result = connection.execute(text("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'notifications'
            """))
            table_exists = result.scalar() > 0
            
            if table_exists:
                print("SUCCESS: 'notifications' table already exists")
                return
            
            # Create notifications table
            print("Creating 'notifications' table...")
            connection.execute(text("""
                CREATE TABLE notifications (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    title NVARCHAR(200) NOT NULL,
                    message NVARCHAR(MAX) NOT NULL,
                    type NVARCHAR(50) NOT NULL,
                    related_id INT NULL,
                    is_read BIT DEFAULT 0,
                    created_at DATETIME2 DEFAULT GETDATE(),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            connection.commit()
            
            print("SUCCESS: 'notifications' table created successfully!")
            
            # Verify table was created
            result = connection.execute(text("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'notifications'
            """))
            table_exists = result.scalar() > 0
            
            if table_exists:
                print("SUCCESS: Verification successful - 'notifications' table exists")
            else:
                print("ERROR: Verification failed - 'notifications' table not found")
                
    except Exception as e:
        print(f"ERROR: Error creating notifications table: {e}")
        raise

if __name__ == "__main__":
    create_notifications_table()
