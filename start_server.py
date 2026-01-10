import uvicorn
import logging
from database import engine, Base
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_tables_created():
    """Ensure all tables exist in blogDb database"""
    try:
        logger.info("Starting Community Skill Swap Platform...")
        logger.info("Database: blogDb")
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DB_NAME()"))
            current_db = result.scalar()
            logger.info(f"Connected to: {current_db}")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Tables ready: users, skills, skill_exchange_requests")
        
        # Quick verification
        with engine.connect() as connection:
            tables = ['users', 'skills', 'skill_exchange_requests']
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'"))
                exists = result.scalar() > 0
                if exists:
                    logger.info(f"✓ {table}")
                else:
                    logger.error(f"✗ {table} missing")
        
        logger.info("Database setup complete!")
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False

if __name__ == "__main__":
    if ensure_tables_created():
        logger.info("🚀 Starting FastAPI server...")
        logger.info("📖 API Docs: http://localhost:8000/docs")
        logger.info("🔍 Database Status: http://localhost:8000/database-status")
        logger.info("🏠 Frontend: Open frontend/index.html in browser")
        
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        logger.error("Failed to start server due to database issues")
