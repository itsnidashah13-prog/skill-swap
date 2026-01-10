"""
Database initialization script for Community Skill Swap Platform
This script will create the database and all required tables in SQL Server
"""

import logging
from sqlalchemy import create_engine, text
from database import Base, settings
from models import User, Skill, SkillExchangeRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_and_tables():
    """Create database and all tables if they don't exist"""
    
    try:
        logger.info("Starting database initialization...")
        
        # Create engine
        engine = create_engine(settings.database_url)
        
        # Test connection
        logger.info("Testing database connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✓ Database connection successful!")
        
        # Create database if it doesn't exist
        logger.info("Creating database if it doesn't exist...")
        try:
            # Extract database name from connection string
            db_name = settings.database_url.split('/')[-1].split('?')[0]
            
            # Connect to master database to create our database
            master_url = settings.database_url.replace(f'/{db_name}', '/master')
            master_engine = create_engine(master_url)
            
            with master_engine.connect() as connection:
                connection.execute(text(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{db_name}') CREATE DATABASE [{db_name}]"))
                connection.commit()
                logger.info(f"✓ Database '{db_name}' created or already exists!")
                
        except Exception as e:
            logger.warning(f"Could not create database (may already exist): {e}")
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ All tables created successfully!")
        
        # Verify tables exist
        logger.info("Verifying table creation...")
        with engine.connect() as connection:
            tables = ['users', 'skills', 'skill_exchange_requests']
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'"))
                count = result.scalar()
                if count > 0:
                    logger.info(f"✓ Table '{table}' exists!")
                else:
                    logger.error(f"✗ Table '{table}' not found!")
        
        logger.info("🎉 Database initialization completed successfully!")
        
        # Print table information
        logger.info("\n=== TABLE STRUCTURES ===")
        logger.info("1. Users Table:")
        logger.info("   - id (PK, INT)")
        logger.info("   - username (VARCHAR(50), UNIQUE)")
        logger.info("   - email (VARCHAR(100), UNIQUE)")
        logger.info("   - password_hash (VARCHAR(255))")
        logger.info("   - full_name (VARCHAR(100))")
        logger.info("   - bio (TEXT)")
        logger.info("   - created_at (DATETIME)")
        logger.info("   - is_active (BOOLEAN)")
        
        logger.info("\n2. Skills Table:")
        logger.info("   - id (PK, INT)")
        logger.info("   - user_id (FK to users)")
        logger.info("   - title (VARCHAR(100))")
        logger.info("   - description (TEXT)")
        logger.info("   - category (VARCHAR(50))")
        logger.info("   - proficiency_level (VARCHAR(20))")
        logger.info("   - created_at (DATETIME)")
        logger.info("   - is_active (BOOLEAN)")
        
        logger.info("\n3. Skill Exchange Requests Table:")
        logger.info("   - id (PK, INT)")
        logger.info("   - skill_id (FK to skills)")
        logger.info("   - requester_id (FK to users)")
        logger.info("   - skill_owner_id (FK to users)")
        logger.info("   - message (TEXT)")
        logger.info("   - status (VARCHAR(20))")
        logger.info("   - created_at (DATETIME)")
        logger.info("   - updated_at (DATETIME)")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    create_database_and_tables()
