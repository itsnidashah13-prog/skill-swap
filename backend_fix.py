#!/usr/bin/env python3
"""
Comprehensive backend fix for Skill Swap application
"""

import sys
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db, settings
from routers import users, skills, exchanges, notifications
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="Community Skill Swap Platform",
        description="A platform for users to share and exchange skills with JWT authentication.",
        version="2.0.0"
    )
    
    # CRITICAL FIX: Enhanced CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:3002",
            "http://localhost:3002", 
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "*"  # Allow all origins for development
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With", "*"],
        expose_headers=["Authorization", "Content-Type"]
    )
    
    # Include routers
    app.include_router(users.router, prefix="/api/users", tags=["users"])
    app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
    app.include_router(exchanges.router, prefix="/api/exchanges", tags=["exchanges"])
    app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
    
    # Health check endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Community Skill Swap Platform API",
            "version": "2.0.0",
            "status": "healthy",
            "endpoints": {
                "users": "/api/users",
                "skills": "/api/skills", 
                "exchanges": "/api/exchanges",
                "health": "/health"
            }
        }
    
    @app.get("/health")
    async def health_check():
        try:
            # Test database connection
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                db_status = "healthy" if result.scalar() == 1 else "unhealthy"
            
            return {
                "status": "healthy",
                "database": db_status,
                "version": "2.0.0",
                "cors": "enabled",
                "authentication": "jwt"
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service unavailable: {str(e)}"
            )
    
    # CRITICAL FIX: Add debug endpoints for troubleshooting
    @app.get("/debug/endpoints")
    async def debug_endpoints():
        """List all available endpoints"""
        return {
            "endpoints": [
                {"path": "/", "method": "GET", "description": "Root endpoint"},
                {"path": "/health", "method": "GET", "description": "Health check"},
                {"path": "/debug/endpoints", "method": "GET", "description": "This endpoint"},
                {"path": "/api/users/register", "method": "POST", "description": "Register user"},
                {"path": "/api/users/login", "method": "POST", "description": "Login user"},
                {"path": "/api/users/me", "method": "GET", "description": "Get current user"},
                {"path": "/api/skills/", "method": "GET", "description": "Get all skills"},
                {"path": "/api/skills/my-skills", "method": "GET", "description": "Get user skills"},
                {"path": "/api/exchanges/", "method": "POST", "description": "Create exchange request"},
                {"path": "/api/exchanges/", "method": "GET", "description": "Get user exchanges"}
            ]
        }
    
    @app.get("/debug/cors")
    async def debug_cors():
        """Debug CORS configuration"""
        return {
            "cors_config": {
                "allow_origins": [
                    "http://127.0.0.1:3002",
                    "http://localhost:3002", 
                    "http://127.0.0.1:3000",
                    "http://localhost:3000",
                    "*"
                ],
                "allow_credentials": True,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
                "allow_headers": ["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With", "*"],
                "expose_headers": ["Authorization", "Content-Type"]
            }
        }
    
    @app.get("/debug/database")
    async def debug_database():
        """Debug database connection and data"""
        try:
            with engine.connect() as connection:
                # Check tables
                tables_query = text("""
                    SELECT TABLE_NAME, TABLE_TYPE 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """)
                tables = connection.execute(tables_query).fetchall()
                
                # Check user count
                user_count = connection.execute(text("SELECT COUNT(*) FROM users")).scalar()
                
                # Check skill count  
                skill_count = connection.execute(text("SELECT COUNT(*) FROM skills")).scalar()
                
                # Check exchange count
                exchange_count = connection.execute(text("SELECT COUNT(*) FROM skill_exchange_requests")).scalar()
                
                return {
                    "database_status": "connected",
                    "tables": [{"name": row[0], "type": row[1]} for row in tables],
                    "record_counts": {
                        "users": user_count,
                        "skills": skill_count,
                        "exchanges": exchange_count
                    }
                }
        except Exception as e:
            logger.error(f"Database debug failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database debug failed: {str(e)}"
            )
    
    # CRITICAL FIX: Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception: {exc}")
        return {
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    
    return app

def create_database_tables():
    """Create database tables if they don't exist"""
    try:
        logger.info("Creating database tables...")
        
        with engine.connect() as connection:
            # Test database connection
            result = connection.execute(text("SELECT DB_NAME()"))
            current_db = result.scalar()
            logger.info(f"Connected to database: {current_db}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully!")
        
        # Verify tables exist
        with engine.connect() as connection:
            tables = ['users', 'skills', 'skill_exchange_requests', 'notifications']
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'"))
                exists = result.scalar() > 0
                logger.info(f"Table '{table}': {'✓ Created' if exists else '✗ Not found'}")
            
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Create the application
app = create_app()

# Create database tables on startup
create_database_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend_fix:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
