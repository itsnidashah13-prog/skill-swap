"""
AI Router for Skill Swap Platform
Provides AI-powered endpoints for skill analysis and matching
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from database import get_db
from models import User, Skill
from schemas import SkillResponse
from routers.users import get_current_user
from gemini_service import gemini_service

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI"])

@router.post("/analyze-skill")
async def analyze_skill(
    title: str,
    description: str,
    category: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze and enhance a skill description using AI
    
    Args:
        title: Skill title
        description: Skill description
        category: Skill category (optional)
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Enhanced skill analysis with AI insights
    """
    try:
        logger.info(f"Analyzing skill '{title}' for user {current_user.username}")
        
        # Use Gemini AI service
        analysis = await gemini_service.analyze_skill_description(title, description, category)
        
        return {
            "success": True,
            "data": analysis,
            "message": "Skill analysis completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze skill: {str(e)}"
        )

@router.post("/categorize-skill")
async def categorize_skill(
    title: str,
    description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Automatically categorize a skill using AI
    
    Args:
        title: Skill title
        description: Skill description
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Suggested category with confidence score
    """
    try:
        logger.info(f"Categorizing skill '{title}' for user {current_user.username}")
        
        # Use Gemini AI service
        categorization = await gemini_service.categorize_skill(title, description)
        
        return {
            "success": True,
            "data": categorization,
            "message": "Skill categorization completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error categorizing skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to categorize skill: {str(e)}"
        )

@router.post("/find-matches")
async def find_skill_matches(
    target_skills: List[Dict[str, str]],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Find skill matches between user's skills and target skills
    
    Args:
        target_skills: List of target skills to match against
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Skill matches with compatibility scores and recommendations
    """
    try:
        logger.info(f"Finding skill matches for user {current_user.username}")
        
        # Get user's skills from database
        user_skills_query = db.query(Skill).filter(Skill.user_id == current_user.id)
        user_skills = user_skills_query.all()
        
        if not user_skills:
            return {
                "success": True,
                "data": {
                    "matches": [],
                    "skill_gaps": ["Add some skills to your profile first"],
                    "learning_path": [],
                    "exchange_suggestions": []
                },
                "message": "No skills found for matching"
            }
        
        # Convert user skills to dict format
        user_skills_dict = [
            {
                "title": skill.title,
                "description": skill.description,
                "category": skill.category,
                "proficiency_level": skill.proficiency_level
            }
            for skill in user_skills
        ]
        
        # Use Gemini AI service for matching
        matches = await gemini_service.find_skill_matches(user_skills_dict, target_skills)
        
        return {
            "success": True,
            "data": matches,
            "message": f"Found {len(matches.get('matches', []))} skill matches"
        }
        
    except Exception as e:
        logger.error(f"Error finding skill matches: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find skill matches: {str(e)}"
        )

@router.get("/my-skills-analysis")
async def get_my_skills_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered analysis of user's skills
    
    Args:
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Comprehensive analysis of user's skills with insights
    """
    try:
        logger.info(f"Getting skills analysis for user {current_user.username}")
        
        # Get user's skills from database
        user_skills_query = db.query(Skill).filter(Skill.user_id == current_user.id)
        user_skills = user_skills_query.all()
        
        if not user_skills:
            return {
                "success": True,
                "data": {
                    "total_skills": 0,
                    "categories": {},
                    "proficiency_levels": {},
                    "recommendations": ["Add some skills to get AI analysis"],
                    "ai_insights": {}
                },
                "message": "No skills found for analysis"
            }
        
        # Analyze skills
        categories = {}
        proficiency_levels = {}
        enhanced_skills = []
        
        for skill in user_skills:
            # Count categories
            if skill.category in categories:
                categories[skill.category] += 1
            else:
                categories[skill.category] = 1
            
            # Count proficiency levels
            if skill.proficiency_level in proficiency_levels:
                proficiency_levels[skill.proficiency_level] += 1
            else:
                proficiency_levels[skill.proficiency_level] = 1
            
            # Get AI analysis for each skill
            try:
                analysis = await gemini_service.analyze_skill_description(
                    skill.title, skill.description, skill.category
                )
                enhanced_skills.append({
                    "id": skill.id,
                    "title": skill.title,
                    "description": skill.description,
                    "category": skill.category,
                    "proficiency_level": skill.proficiency_level,
                    "ai_analysis": analysis
                })
            except Exception as e:
                logger.warning(f"Failed to analyze skill {skill.id}: {e}")
                enhanced_skills.append({
                    "id": skill.id,
                    "title": skill.title,
                    "description": skill.description,
                    "category": skill.category,
                    "proficiency_level": skill.proficiency_level,
                    "ai_analysis": None
                })
        
        # Generate recommendations
        recommendations = []
        
        # Category diversity recommendation
        if len(categories) < 3:
            recommendations.append("Consider adding skills from different categories to diversify your profile")
        
        # Proficiency progression
        if proficiency_levels.get("Beginner", 0) > proficiency_levels.get("Advanced", 0):
            recommendations.append("Focus on advancing your beginner skills to intermediate level")
        
        # Skill gaps
        if len(user_skills) < 5:
            recommendations.append("Add more skills to increase your exchange opportunities")
        
        return {
            "success": True,
            "data": {
                "total_skills": len(user_skills),
                "categories": categories,
                "proficiency_levels": proficiency_levels,
                "enhanced_skills": enhanced_skills,
                "recommendations": recommendations,
                "ai_available": gemini_service.is_available()
            },
            "message": "Skills analysis completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error getting skills analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get skills analysis: {str(e)}"
        )

@router.get("/ai-status")
async def get_ai_status():
    """
    Get the status of AI services
    
    Returns:
        AI service availability and configuration status
    """
    try:
        return {
            "success": True,
            "data": {
                "ai_available": gemini_service.is_available(),
                "service_name": "Gemini AI",
                "model": "gemini-1.5-flash",
                "features": [
                    "Skill description analysis",
                    "Automatic skill categorization",
                    "Skill matching and recommendations",
                    "Skills portfolio analysis"
                ]
            },
            "message": "AI status retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error getting AI status: {e}")
        return {
            "success": False,
            "data": None,
            "message": f"Failed to get AI status: {str(e)}"
        }

@router.post("/enhance-description")
async def enhance_skill_description(
    title: str,
    description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enhance a skill description using AI
    
    Args:
        title: Skill title
        description: Current skill description
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Enhanced skill description with AI suggestions
    """
    try:
        logger.info(f"Enhancing description for skill '{title}'")
        
        # Use Gemini AI service
        analysis = await gemini_service.analyze_skill_description(title, description)
        
        return {
            "success": True,
            "data": {
                "original_description": description,
                "enhanced_description": analysis.get("enhanced_description", description),
                "keywords": analysis.get("keywords", []),
                "applications": analysis.get("applications", []),
                "suggested_proficiency": analysis.get("suggested_proficiency", "Intermediate")
            },
            "message": "Description enhanced successfully"
        }
        
    except Exception as e:
        logger.error(f"Error enhancing description: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enhance description: {str(e)}"
        )
