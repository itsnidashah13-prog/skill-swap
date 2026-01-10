#!/usr/bin/env python3
"""
Script to add the 'value' column to the skills table
"""

import pyodbc
from sqlalchemy import create_engine, text
from database import settings

def add_value_column():
    """Add value column to skills table"""
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as connection:
            # Check if column already exists
            result = connection.execute(text("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'skills' AND COLUMN_NAME = 'value'
            """))
            column_exists = result.scalar() > 0
            
            if column_exists:
                print("SUCCESS: 'value' column already exists in skills table")
                return
            
            # Add the value column
            print("Adding 'value' column to skills table...")
            connection.execute(text("""
                ALTER TABLE skills 
                ADD value INT DEFAULT 0
            """))
            connection.commit()
            
            print("SUCCESS: 'value' column added successfully!")
            
            # Verify the column was added
            result = connection.execute(text("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'skills' AND COLUMN_NAME = 'value'
            """))
            column_exists = result.scalar() > 0
            
            if column_exists:
                print("SUCCESS: Verification successful - 'value' column exists")
            else:
                print("ERROR: Verification failed - 'value' column not found")
                
    except Exception as e:
        print(f"ERROR: Error adding value column: {e}")
        raise

if __name__ == "__main__":
    add_value_column()
