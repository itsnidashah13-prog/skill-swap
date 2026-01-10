"""
Simple FastAPI Admin Interface - No templates required
Provides REST API endpoints for admin operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List
import hashlib

from database import get_db
from models import User, Skill, SkillExchangeRequest
from crud import (
    get_users, get_user, create_user, update_user, delete_user,
    get_skills, get_skill, create_skill, update_skill, delete_skill,
    get_skill_exchange_requests, get_skill_exchange_request, update_skill_exchange_request,
    get_user_by_username
)
from schemas import UserCreate, UserUpdate, SkillCreate, SkillUpdate
from routers.users import hash_password

# Create router for admin
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Simple admin authentication
security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Simple admin authentication"""
    # Create admin user if doesn't exist
    admin_username = "admin"
    admin_password = "admin123"
    
    if credentials.username == admin_username:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid admin credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

# Admin dashboard - JSON response
@admin_router.get("/")
async def admin_dashboard(db: Session = Depends(get_db), admin: bool = Depends(verify_admin)):
    """Admin dashboard with statistics"""
    
    # Get statistics
    user_count = len(get_users(db, skip=0, limit=1000))
    skill_count = len(get_skills(db, skip=0, limit=1000))
    request_count = len(get_skill_exchange_requests(db, skip=0, limit=1000))
    
    # Get recent items
    recent_users = get_users(db, skip=0, limit=5)
    recent_skills = get_skills(db, skip=0, limit=5)
    recent_requests = get_skill_exchange_requests(db, skip=0, limit=5)
    
    return {
        "message": "Welcome to Skill Swap Admin Dashboard",
        "stats": {
            "users": user_count,
            "skills": skill_count,
            "requests": request_count
        },
        "recent_users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at.isoformat() if user.created_at else None
            } for user in recent_users
        ],
        "recent_skills": [
            {
                "id": skill.id,
                "title": skill.title,
                "category": skill.category,
                "proficiency_level": skill.proficiency_level,
                "created_at": skill.created_at.isoformat() if skill.created_at else None
            } for skill in recent_skills
        ],
        "recent_requests": [
            {
                "id": req.id,
                "status": req.status,
                "created_at": req.created_at.isoformat() if req.created_at else None
            } for req in recent_requests
        ]
    }

# Users management
@admin_router.get("/users")
async def admin_users(db: Session = Depends(get_db), admin: bool = Depends(verify_admin)):
    """Get all users"""
    users = get_users(db, skip=0, limit=100)
    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "bio": user.bio,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            } for user in users
        ]
    }

@admin_router.get("/users/{user_id}")
async def admin_user_detail(user_id: int, db: Session = Depends(get_db), admin: bool = Depends(verify_admin)):
    """Get user details"""
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@admin_router.post("/users")
async def admin_create_user(
    user: UserCreate, 
    db: Session = Depends(get_db), 
    admin: bool = Depends(verify_admin)
):
    """Create new user"""
    return create_user(db, user)

# Skills management
@admin_router.get("/skills")
async def admin_skills(db: Session = Depends(get_db), admin: bool = Depends(verify_admin)):
    """Get all skills"""
    skills = get_skills(db, skip=0, limit=100)
    return {
        "skills": [
            {
                "id": skill.id,
                "title": skill.title,
                "description": skill.description,
                "category": skill.category,
                "proficiency_level": skill.proficiency_level,
                "value": skill.value,
                "is_active": skill.is_active,
                "user_id": skill.user_id,
                "created_at": skill.created_at.isoformat() if skill.created_at else None
            } for skill in skills
        ]
    }

@admin_router.post("/skills")
async def admin_create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin)
):
    """Create new skill"""
    # Create skill for admin user (user ID 1 or create admin user first)
    admin_user = get_user_by_username(db, "admin")
    if not admin_user:
        # Create admin user
        admin_data = UserCreate(
            username="admin",
            email="admin@skillswap.com",
            full_name="System Administrator",
            password="admin123",
            bio="Default admin user"
        )
        admin_user = create_user(db, admin_data)
    
    return create_skill(db, skill, user_id=admin_user.id)

@admin_router.put("/skills/{skill_id}")
async def admin_update_skill(
    skill_id: int,
    skill: SkillUpdate,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin)
):
    """Update skill"""
    return update_skill(db, skill_id, skill)

@admin_router.delete("/skills/{skill_id}")
async def admin_delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin)
):
    """Delete skill"""
    delete_skill(db, skill_id)
    return {"message": "Skill deleted successfully"}

# Exchange requests management
@admin_router.get("/requests")
async def admin_requests(db: Session = Depends(get_db), admin: bool = Depends(verify_admin)):
    """Get all exchange requests"""
    requests = get_skill_exchange_requests(db, skip=0, limit=100)
    return {
        "requests": [
            {
                "id": req.id,
                "skill_id": req.skill_id,
                "requester_id": req.requester_id,
                "skill_owner_id": req.skill_owner_id,
                "status": req.status,
                "message": req.message,
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "updated_at": req.updated_at.isoformat() if req.updated_at else None
            } for req in requests
        ]
    }

@admin_router.put("/requests/{request_id}")
async def admin_update_request(
    request_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin)
):
    """Update exchange request status"""
    from schemas import SkillExchangeRequestUpdate
    update_data = SkillExchangeRequestUpdate(status=status_update.get("status"))
    return update_skill_exchange_request(db, request_id, update_data)

# Create admin user if it doesn't exist
def create_admin_user(db: Session):
    """Create default admin user if it doesn't exist"""
    admin_user = get_user_by_username(db, "admin")
    if not admin_user:
        admin_data = UserCreate(
            username="admin",
            email="admin@skillswap.com",
            full_name="System Administrator",
            password="admin123",
            bio="Default admin user for Skill Swap platform"
        )
        create_user(db, admin_data)
        print("✅ Created default admin user: admin / admin123")
        return True
    return False
