from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, Base, get_db, SessionLocal, Settings
from routers import users, skills, exchanges, notifications, ai
from SIMPLE_ADMIN_FIXED import simple_admin_router
from admin_auth_endpoint import admin_auth_router
from crud import get_user_by_username, get_skill, create_skill_exchange_request, create_notification
from schemas import SkillExchangeRequestCreate, NotificationCreate
import logging
import jwt

# Settings instance
settings = Settings()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_tables():
    """Create database tables if they don't exist"""
    try:
        logger.info("Connecting to blogDb database...")
        
        # Test database connection first
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DB_NAME()"))
            current_db = result.scalar()
            logger.info(f"Connected to database: {current_db}")
        
        # Create all tables
        logger.info("Creating tables: users, skills, skill_exchange_requests")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully in blogDb!")
        
        # Verify tables exist
        with engine.connect() as connection:
            tables = ['users', 'skills', 'skill_exchange_requests']
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'"))
                exists = result.scalar() > 0
                logger.info(f"Table '{table}': {'✓ Created' if exists else '✗ Not found'}")
            
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Create database tables on startup
create_database_tables()

app = FastAPI(
    title="Community Skill Swap Platform",
    description="""
    A platform for users to share and exchange skills with JWT authentication.
    
    ## Authentication
    1. Register a new user via `/users/register`
    2. Login via `/users/login` to get JWT token
    3. Click 'Authorize' button above and paste your token
    4. Use the token to access protected endpoints
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_components={
        "securitySchemes": {
            "JWTAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "**Enter your JWT token** (copy the access_token from login response, paste it here WITH 'Bearer ' prefix: Bearer your_token_here)"
            }
        }
    },
    openapi_security=[{"JWTAuth": []}]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3002", "http://localhost:3002", "http://127.0.0.1:3000", "http://localhost:3000", 
                   "http://127.0.0.1:3005", "http://localhost:3005", "http://127.0.0.1:3006", "http://localhost:3006",
                   "http://127.0.0.1:3007", "http://localhost:3007", "http://127.0.0.1:3008", "http://localhost:3008",
                   "*"],  # Allow all admin dashboard ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "*"],
)

# Include admin auth router FIRST (before other routes)
app.include_router(admin_auth_router)

# Include simple admin router
app.include_router(simple_admin_router)

# Include users router WITH /users prefix (as requested for registration)
app.include_router(users.router, prefix="/users")

# Include other routers with API prefixes
app.include_router(skills.router, prefix="/api/skills")
app.include_router(exchanges.router, prefix="/api/exchanges")
app.include_router(notifications.router, prefix="/api/notifications")
app.include_router(ai.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Community Skill Swap Platform API"}

from pydantic import BaseModel

class Request(BaseModel):
    message: str
    skill_id: int

@app.post("/request-skill")
async def direct_request_skill(
    request: Request,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """
    Direct endpoint for skill requests as requested
    Matches frontend call to http://127.0.0.1:8000/request-skill
    """
    try:
        print(f"DEBUG: Received skill exchange request")
        print(f"DEBUG: Authorization header: {authorization}")
        
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            print(f"ERROR: Invalid authorization header: {authorization}")
            raise HTTPException(
                status_code=401, 
                detail="Authorization header required with Bearer token"
            )
        
        token = authorization.split(" ")[1]
        print(f"DEBUG: Extracted token: {token[:30]}...")
        
        # Decode JWT token to get user
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            print(f"DEBUG: Decoded username: {username}")
            
            if username is None:
                print(f"ERROR: No username in token payload")
                raise HTTPException(status_code=401, detail="Invalid token")
                
        except jwt.ExpiredSignatureError:
            print(f"ERROR: Token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"ERROR: Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Get user from database
        user = get_user_by_username(db, username=username)
        if user is None:
            print(f"ERROR: User not found in database: {username}")
            raise HTTPException(status_code=401, detail="User not found")
        
        print(f"DEBUG: Found user: {user.username} (ID: {user.id})")
        
        # Extract request data
        message = request.message.strip()
        skill_id = request.skill_id
        
        print(f"DEBUG: Request data - skill_id: {skill_id}, message: '{message}'")
        
        if not message:
            print(f"ERROR: Empty message")
            raise HTTPException(status_code=400, detail="Message is required")
        
        if not skill_id:
            print(f"ERROR: Invalid skill_id: {skill_id}")
            raise HTTPException(status_code=400, detail="Skill ID is required")
        
        # Check if skill exists
        skill = get_skill(db, skill_id=skill_id)
        if not skill:
            print(f"ERROR: Skill not found: {skill_id}")
            raise HTTPException(status_code=404, detail="Skill not found")
        
        print(f"DEBUG: Found skill: {skill.title} (ID: {skill.id}, Owner: {skill.user_id})")
        
        # Check if user is not requesting their own skill
        if skill.user_id == user.id:
            print(f"ERROR: User requesting own skill: {skill.user_id} == {user.id}")
            raise HTTPException(status_code=400, detail="Cannot request your own skill")
        
        # Create exchange request
        skill_request = SkillExchangeRequestCreate(
            skill_id=skill_id,
            message=message
        )
        
        print(f"DEBUG: Creating exchange request...")
        db_request = create_skill_exchange_request(
            db, 
            request=skill_request, 
            requester_id=user.id, 
            skill_owner_id=skill.user_id
        )
        
        print(f"DEBUG: Exchange request created with ID: {db_request.id}")
        
        # Create notification for skill owner
        try:
            print(f"DEBUG: Creating notification for skill owner...")
            notification = NotificationCreate(
                title="New Skill Exchange Request",
                message=f"{user.full_name or user.username} wants to learn your skill: {skill.title}",
                type="exchange_request",
                related_id=db_request.id,
                user_id=skill.user_id
            )
            create_notification(db, notification)
            print(f"DEBUG: Notification created successfully")
            
        except Exception as e:
            print(f"ERROR: Notification creation failed: {e}")
            print(f"ERROR: Exception type: {type(e).__name__}")
            print(f"ERROR: Exception details: {str(e)}")
            # Don't re-raise - notification failure shouldn't crash the request
            print("WARNING: Continuing without notification...")
        
        print(f"DEBUG: Preparing response...")
        skill_owner_username = skill.owner.username if skill.owner else "Unknown"
        print(f"DEBUG: Skill owner username: {skill_owner_username}")
        
        return {
            "success": True,
            "message": "Skill request sent successfully",
            "request_id": db_request.id,
            "skill_title": skill.title,
            "skill_owner": skill_owner_username
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error in direct_request_skill: {e}")
        print(f"ERROR: Exception type: {type(e).__name__}")
        print(f"ERROR: Exception details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "healthy"}

@app.get("/database-status")
async def database_status():
    """Check database connection and table status"""
    try:
        with engine.connect() as connection:
            # Check if tables exist
            tables = ['users', 'skills', 'skill_exchange_requests']
            table_status = {}
            
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'"))
                table_status[table] = result.scalar() > 0
            
            return {
                "database_connected": True,
                "tables": table_status,
                "message": "Database connection successful"
            }
    except Exception as e:
        return {
            "database_connected": False,
            "error": str(e),
            "message": "Database connection failed"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
