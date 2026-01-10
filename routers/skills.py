from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User
from schemas import SkillCreate, SkillResponse, SkillUpdate
from crud import create_skill, get_skill, get_skills, get_skills_by_user, update_skill, delete_skill
from routers.users import get_current_user

router = APIRouter(tags=["skills"])

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED, dependencies=[Security(get_current_user)])
async def create_skill_endpoint(
    skill: SkillCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new skill for the authenticated user.
    
    Args:
        skill: Skill data to create
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created skill object
        
    Raises:
        HTTPException: If validation fails or user not authorized
    """
    try:
        print(f"Creating skill for user {current_user.id}: {skill.title}")
        
        # Validate skill data
        if not skill.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill title cannot be empty"
            )
        
        if not skill.description.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill description cannot be empty"
            )
        
        if not skill.category.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill category cannot be empty"
            )
        
        if skill.proficiency_level not in ["Beginner", "Intermediate", "Advanced", "Expert"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Proficiency level must be one of: Beginner, Intermediate, Advanced, Expert"
            )
        
        # Validate value field
        if skill.value is not None and (skill.value < 0 or skill.value > 1000):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill value must be between 0 and 1000"
            )
        
        created_skill = create_skill(db=db, skill=skill, user_id=current_user.id)
        print(f"Skill created successfully with ID: {created_skill.id}")
        return created_skill
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the skill"
        )

@router.get("/", response_model=List[SkillResponse])
async def read_skills(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    skills = get_skills(db, skip=skip, limit=limit, category=category)
    return skills

@router.get("/my-skills", response_model=List[SkillResponse], dependencies=[Security(get_current_user)])
async def read_my_skills(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skills = get_skills_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return skills

@router.get("/{skill_id}", response_model=SkillResponse)
async def read_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = get_skill(db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill

@router.put("/{skill_id}", response_model=SkillResponse, dependencies=[Security(get_current_user)])
async def update_skill_endpoint(
    skill_id: int, 
    skill_update: SkillUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if skill exists and belongs to current user
    db_skill = get_skill(db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    if db_skill.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this skill"
        )
    
    updated_skill = update_skill(db, skill_id=skill_id, skill_update=skill_update)
    return updated_skill

@router.delete("/{skill_id}", response_model=SkillResponse, dependencies=[Security(get_current_user)])
async def delete_skill_endpoint(
    skill_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if skill exists and belongs to current user
    db_skill = get_skill(db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    if db_skill.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this skill"
        )
    
    deleted_skill = delete_skill(db, skill_id=skill_id)
    return deleted_skill
