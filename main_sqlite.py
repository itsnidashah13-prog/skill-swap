# SQLite version of main.py for easy development
# Use this instead of main.py if you don't have SQL Server setup

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database_sqlite import engine, Base, get_db
from routers import users, skills, exchanges
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_tables():
    """Create database tables if they don't exist"""
    try:
        logger.info("Creating SQLite database tables...")
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✓ SQLite database tables created successfully!")
        
        # Test database connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✓ SQLite database connection test successful!")
            
    except Exception as e:
        logger.error(f"Error creating SQLite database tables: {e}")
        raise

# Create database tables on startup
create_database_tables()

app = FastAPI(
    title="Community Skill Swap Platform (SQLite)",
    description="A platform for users to share and exchange skills - SQLite Version",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - in production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(skills.router)
app.include_router(exchanges.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Community Skill Swap Platform API (SQLite Version)"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "SQLite"}

@app.get("/database-status")
async def database_status():
    """Check database connection and table status"""
    try:
        with engine.connect() as connection:
            # Check if tables exist
            tables = ['users', 'skills', 'skill_exchange_requests']
            table_status = {}
            
            for table in tables:
                result = connection.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
                table_status[table] = result.fetchone() is not None
            
            return {
                "database_connected": True,
                "database_type": "SQLite",
                "tables": table_status,
                "message": "SQLite database connection successful"
            }
    except Exception as e:
        return {
            "database_connected": False,
            "error": str(e),
            "message": "SQLite database connection failed"
        }

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FastAPI with SQLite database...")
    logger.info("📖 API Documentation: http://localhost:8000/docs")
    logger.info("🔍 Database Status: http://localhost:8000/database-status")
    uvicorn.run(app, host="0.0.0.0", port=8000)
