"""
FastAPI Admin Interface for Skill Swap Application
This provides a web-based admin panel similar to Django admin
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import hashlib

from database import get_db, SessionLocal
from models import User, Skill, SkillExchangeRequest, Notification
from crud import (
    get_users, get_user, create_user, update_user, delete_user,
    get_skills, get_skill, create_skill, update_skill, delete_skill,
    get_skill_exchange_requests, get_skill_exchange_request, update_skill_exchange_request,
    create_notification, get_user_by_username
)
from schemas import UserCreate, UserUpdate, SkillCreate, SkillUpdate
from routers.users import get_current_user, hash_password

# Create router for admin
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Setup templates (you'll need to create an admin/templates folder)
templates = Jinja2Templates(directory="admin/templates")

# Simple admin authentication (you should improve this in production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def verify_admin_auth(request: Request):
    """Simple admin authentication check"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        return None
    
    import base64
    try:
        decoded = base64.b64decode(auth_header[6:]).decode()
        username, password = decoded.split(":")
        
        if username == ADMIN_USERNAME and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            return username
    except:
        pass
    
    return None

# Admin login page
@admin_router.get("/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Admin dashboard
@admin_router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    # Check admin authentication
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    # Get statistics
    user_count = len(get_users(db, skip=0, limit=1000))
    skill_count = len(get_skills(db, skip=0, limit=1000))
    request_count = len(get_skill_exchange_requests(db, skip=0, limit=1000))
    
    # Get recent items
    recent_users = get_users(db, skip=0, limit=5)
    recent_skills = get_skills(db, skip=0, limit=5)
    recent_requests = get_skill_exchange_requests(db, skip=0, limit=5)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "admin_user": admin_user,
        "stats": {
            "users": user_count,
            "skills": skill_count,
            "requests": request_count
        },
        "recent_users": recent_users,
        "recent_skills": recent_skills,
        "recent_requests": recent_requests
    })

# Users management
@admin_router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, db: Session = Depends(get_db)):
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    users = get_users(db, skip=0, limit=100)
    return templates.TemplateResponse("users.html", {
        "request": request,
        "admin_user": admin_user,
        "users": users
    })

@admin_router.get("/users/{user_id}", response_class=HTMLResponse)
async def admin_user_detail(request: Request, user_id: int, db: Session = Depends(get_db)):
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return templates.TemplateResponse("user_detail.html", {
        "request": request,
        "admin_user": admin_user,
        "user": user
    })

# Skills management
@admin_router.get("/skills", response_class=HTMLResponse)
async def admin_skills(request: Request, db: Session = Depends(get_db)):
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    skills = get_skills(db, skip=0, limit=100)
    return templates.TemplateResponse("skills.html", {
        "request": request,
        "admin_user": admin_user,
        "skills": skills
    })

@admin_router.get("/skills/new", response_class=HTMLResponse)
async def admin_skill_new(request: Request, db: Session = Depends(get_db)):
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    users = get_users(db, skip=0, limit=100)
    return templates.TemplateResponse("skill_form.html", {
        "request": request,
        "admin_user": admin_user,
        "users": users,
        "skill": None
    })

@admin_router.post("/skills/new")
async def admin_skill_create(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    proficiency_level: str = Form(...),
    user_id: int = Form(...),
    value: int = Form(1)
):
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    skill_data = SkillCreate(
        title=title,
        description=description,
        category=category,
        proficiency_level=proficiency_level,
        value=value
    )
    
    # Create skill for specified user
    skill = create_skill(db, skill_data, user_id=user_id)
    
    return RedirectResponse(url="/admin/skills", status_code=302)

# Exchange requests management
@admin_router.get("/requests", response_class=HTMLResponse)
async def admin_requests(request: Request, db: Session = Depends(get_db)):
    admin_user = verify_admin_auth(request)
    if not admin_user:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    requests = get_skill_exchange_requests(db, skip=0, limit=100)
    return templates.TemplateResponse("requests.html", {
        "request": request,
        "admin_user": admin_user,
        "requests": requests
    })

# API endpoints for admin operations
@admin_router.post("/api/skills")
async def admin_create_skill_api(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """API endpoint to create skills via admin interface"""
    return create_skill(db, skill, user_id=current_user.id)

@admin_router.put("/api/skills/{skill_id}")
async def admin_update_skill_api(
    skill_id: int,
    skill: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """API endpoint to update skills via admin interface"""
    return update_skill(db, skill_id, skill)

@admin_router.delete("/api/skills/{skill_id}")
async def admin_delete_skill_api(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """API endpoint to delete skills via admin interface"""
    delete_skill(db, skill_id)
    return {"message": "Skill deleted successfully"}

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
