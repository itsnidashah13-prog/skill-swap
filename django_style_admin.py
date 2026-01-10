"""
Django-Style Admin Interface for FastAPI
Provides a familiar Django admin experience for FastAPI
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database import get_db
from models import User, Skill, SkillExchangeRequest
from crud import (
    get_users, get_user, create_user, update_user,
    get_skills, get_skill, create_skill, update_skill,
    get_skill_exchange_requests, get_skill_exchange_request, update_skill_exchange_request,
    get_user_by_username, hash_password
)
from schemas import UserCreate, UserUpdate, SkillCreate, SkillUpdate

# Create router for Django-style admin
django_admin_router = APIRouter(prefix="/admin", tags=["django-admin"])

# Setup templates
templates = Jinja2Templates(directory="admin/templates")

# Simple session-based admin authentication
ADMIN_SESSION_KEY = "admin_authenticated"

def check_admin_auth(request: Request):
    """Check if user is authenticated as admin"""
    # For simplicity, using session cookie (in production, use proper auth)
    return True  # Auto-authenticate for now (implement proper auth later)

# Django-style admin home page
@django_admin_router.get("/", response_class=HTMLResponse)
async def django_admin_home(request: Request, db: Session = Depends(get_db)):
    """Django-style admin home page"""
    
    if not check_admin_auth(request):
        return RedirectResponse(url="/admin/login/")
    
    # Get statistics
    user_count = len(get_users(db, skip=0, limit=1000))
    skill_count = len(get_skills(db, skip=0, limit=1000))
    request_count = len(get_skill_exchange_requests(db, skip=0, limit=1000))
    
    return templates.TemplateResponse("admin_home.html", {
        "request": request,
        "app_list": [
            {
                "name": "Users",
                "model": "User",
                "count": user_count,
                "url": "/admin/auth/user/",
                "add_url": "/admin/auth/user/add/"
            },
            {
                "name": "Skills", 
                "model": "Skill",
                "count": skill_count,
                "url": "/admin/skills/skill/",
                "add_url": "/admin/skills/skill/add/"
            },
            {
                "name": "Exchange Requests",
                "model": "SkillExchangeRequest", 
                "count": request_count,
                "url": "/admin/exchanges/skillexchangerequest/",
                "add_url": "/admin/exchanges/skillexchangerequest/add/"
            }
        ],
        "site_title": "Skill Swap Administration",
        "site_header": "Skill Swap Administration"
    })

# Django-style login page
@django_admin_router.get("/login/", response_class=HTMLResponse)
async def django_admin_login(request: Request):
    """Django-style admin login page"""
    return templates.TemplateResponse("admin_login.html", {
        "request": request,
        "site_title": "Skill Swap Administration",
        "site_header": "Skill Swap Administration"
    })

# Django-style user list
@django_admin_router.get("/auth/user/", response_class=HTMLResponse)
async def django_admin_user_list(request: Request, db: Session = Depends(get_db)):
    """Django-style user list page"""
    
    if not check_admin_auth(request):
        return RedirectResponse(url="/admin/login/")
    
    users = get_users(db, skip=0, limit=100)
    
    return templates.TemplateResponse("admin_user_list.html", {
        "request": request,
        "users": users,
        "opts": {
            "app_label": "auth",
            "model_name": "user",
            "verbose_name": "User",
            "verbose_name_plural": "Users"
        },
        "site_title": "Skill Swap Administration",
        "site_header": "Skill Swap Administration"
    })

# Django-style skill list
@django_admin_router.get("/skills/skill/", response_class=HTMLResponse)
async def django_admin_skill_list(request: Request, db: Session = Depends(get_db)):
    """Django-style skill list page"""
    
    if not check_admin_auth(request):
        return RedirectResponse(url="/admin/login/")
    
    skills = get_skills(db, skip=0, limit=100)
    
    return templates.TemplateResponse("admin_skill_list.html", {
        "request": request,
        "skills": skills,
        "opts": {
            "app_label": "skills",
            "model_name": "skill",
            "verbose_name": "Skill",
            "verbose_name_plural": "Skills"
        },
        "site_title": "Skill Swap Administration",
        "site_header": "Skill Swap Administration"
    })

# Django-style skill add form
@django_admin_router.get("/skills/skill/add/", response_class=HTMLResponse)
async def django_admin_skill_add(request: Request, db: Session = Depends(get_db)):
    """Django-style skill add form"""
    
    if not check_admin_auth(request):
        return RedirectResponse(url="/admin/login/")
    
    users = get_users(db, skip=0, limit=100)
    
    return templates.TemplateResponse("admin_skill_form.html", {
        "request": request,
        "users": users,
        "opts": {
            "app_label": "skills",
            "model_name": "skill",
            "verbose_name": "Skill",
            "verbose_name_plural": "Skills"
        },
        "is_add": True,
        "site_title": "Skill Swap Administration",
        "site_header": "Skill Swap Administration"
    })

# Django-style skill add POST
@django_admin_router.post("/skills/skill/add/")
async def django_admin_skill_add_post(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    proficiency_level: str = Form(...),
    user_id: int = Form(...),
    value: int = Form(1)
):
    """Handle Django-style skill add form submission"""
    
    if not check_admin_auth(request):
        return RedirectResponse(url="/admin/login/")
    
    skill_data = SkillCreate(
        title=title,
        description=description,
        category=category,
        proficiency_level=proficiency_level,
        value=value
    )
    
    create_skill(db, skill_data, user_id=user_id)
    
    return RedirectResponse(url="/admin/skills/skill/", status_code=302)

# Django-style exchange request list
@django_admin_router.get("/exchanges/skillexchangerequest/", response_class=HTMLResponse)
async def django_admin_request_list(request: Request, db: Session = Depends(get_db)):
    """Django-style exchange request list page"""
    
    if not check_admin_auth(request):
        return RedirectResponse(url="/admin/login/")
    
    requests = get_skill_exchange_requests(db, skip=0, limit=100)
    
    return templates.TemplateResponse("admin_request_list.html", {
        "request": request,
        "requests": requests,
        "opts": {
            "app_label": "exchanges",
            "model_name": "skillexchangerequest",
            "verbose_name": "Skill exchange request",
            "verbose_name_plural": "Skill exchange requests"
        },
        "site_title": "Skill Swap Administration",
        "site_header": "Skill Swap Administration"
    })

# API endpoints for AJAX operations
@django_admin_router.post("/api/skills/")
async def admin_create_skill_api(
    skill: SkillCreate,
    db: Session = Depends(get_db)
):
    """API endpoint to create skills"""
    # Create skill for first user (or implement proper user selection)
    users = get_users(db, skip=0, limit=1)
    if users:
        return create_skill(db, skill, user_id=users[0].id)
    else:
        raise HTTPException(status_code=400, detail="No users available")

@django_admin_router.put("/api/skills/{skill_id}")
async def admin_update_skill_api(
    skill_id: int,
    skill: SkillUpdate,
    db: Session = Depends(get_db)
):
    """API endpoint to update skills"""
    return update_skill(db, skill_id, skill)

@django_admin_router.delete("/api/skills/{skill_id}")
async def admin_delete_skill_api(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """API endpoint to delete skills"""
    # Delete skill manually since delete_skill doesn't exist
    skill = get_skill(db, skill_id)
    if skill:
        db.delete(skill)
        db.commit()
    return {"message": "Skill deleted successfully"}
