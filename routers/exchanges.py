from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Skill, SkillExchangeRequest
from schemas import SkillExchangeRequestCreate, SkillExchangeRequestUpdate, SkillExchangeRequestResponse
from crud import (
    create_skill_exchange_request, 
    get_skill_exchange_requests_for_user,
    get_skill, 
    get_skill_exchange_request, 
    update_skill_exchange_request,
    update_skill_exchange_request_status,
    create_notification
)
from routers.users import get_current_user

router = APIRouter(tags=["skill-exchanges"])

@router.post("/", response_model=SkillExchangeRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_exchange_request(
    request: SkillExchangeRequestCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if skill exists
    skill = get_skill(db, skill_id=request.skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Check if user is not requesting their own skill
    if skill.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot request your own skill")
    
    # Create exchange request
    db_request = create_skill_exchange_request(
        db, 
        request=request, 
        requester_id=current_user.id, 
        skill_owner_id=skill.user_id
    )
    
    # Create notification for skill owner
    try:
        notification = NotificationCreate(
            title="New Skill Exchange Request",
            message=f"{current_user.full_name or current_user.username} wants to learn your skill: {skill.title}",
            type="exchange_request",
            related_id=db_request.id,
            user_id=skill.user_id
        )
        create_notification(db, notification)
    except Exception as e:
        # Log notification error but don't fail the request
        print(f"Notification creation failed: {e}")
    
    return db_request

@router.post("/request-skill", response_model=SkillExchangeRequestResponse, status_code=status.HTTP_201_CREATED)
async def request_skill(
    request: SkillExchangeRequestCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Alternative endpoint for skill exchange requests
    Matches the frontend call to /exchanges/request-skill
    """
    # Check if skill exists
    skill = get_skill(db, skill_id=request.skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Check if user is not requesting their own skill
    if skill.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot request your own skill")
    
    # Create exchange request
    db_request = create_skill_exchange_request(
        db, 
        request=request, 
        requester_id=current_user.id, 
        skill_owner_id=skill.user_id
    )
    
    # Create notification for skill owner
    try:
        notification = NotificationCreate(
            title="New Skill Exchange Request",
            message=f"{current_user.full_name or current_user.username} wants to learn your skill: {skill.title}",
            type="exchange_request",
            related_id=db_request.id,
            user_id=skill.user_id
        )
        create_notification(db, notification)
    except Exception as e:
        # Log notification error but don't fail the request
        print(f"Notification creation failed: {e}")
    
    return db_request

@router.get("/", response_model=List[dict])
async def read_exchange_requests(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requests = get_skill_exchange_requests_for_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return requests

@router.get("/all", response_model=List[dict])
async def read_all_exchange_requests(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requests = get_skill_exchange_requests(db, skip=skip, limit=limit, status=status)
    return requests

@router.get("/{request_id}", response_model=SkillExchangeRequestResponse)
async def read_exchange_request(
    request_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    request = get_skill_exchange_request(db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Exchange request not found")
    
    # Check if user is involved in this request
    if request.requester_id != current_user.id and request.skill_owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    
    return request

@router.put("/{request_id}", response_model=SkillExchangeRequestResponse)
async def update_exchange_request(
    request_id: int,
    request_update: SkillExchangeRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    request = get_skill_exchange_request(db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Exchange request not found")
    
    # Only skill owner can update request status
    if request.skill_owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this request")
    
    updated_request = update_skill_exchange_request(db, request_id=request_id, request_update=request_update)
    
    # Create notification for requester if status changed
    if request_update.status and request_update.status != request.status:
        notification_data = {
            "title": f"Exchange Request {request_update.status.title()}",
            "message": f"Your exchange request for '{request.skill.title}' has been {request_update.status}",
            "type": "exchange_update",
            "related_id": request_id,
            "user_id": request.requester_id
        }
        
        try:
            create_notification(db, notification_data)
        except Exception as e:
            print(f"Notification creation failed: {e}")
    
    return updated_request

@router.delete("/{request_id}")
async def delete_exchange_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    request = get_skill_exchange_request(db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Exchange request not found")
    
    # Only requester can delete their own request
    if request.requester_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this request")
    
    # Soft delete by updating status
    update_data = SkillExchangeRequestUpdate(status="cancelled")
    updated_request = update_skill_exchange_request(db, request_id=request_id, request_update=update_data)
    
    return {"message": "Exchange request deleted successfully"}

@router.patch("/requests/{request_id}", response_model=dict)
async def update_request_status(
    request_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the status of a skill exchange request (Accept/Reject)
    Only the skill owner can update the request status
    """
    try:
        # Get the new status from request body
        new_status = status_update.get("status")
        
        if new_status not in ["Accepted", "Rejected"]:
            raise HTTPException(status_code=400, detail="Invalid status. Must be 'Accepted' or 'Rejected'")
        
        # Get the request
        request = db.query(SkillExchangeRequest).filter(SkillExchangeRequest.id == request_id).first()
        
        if not request:
            raise HTTPException(status_code=404, detail="Exchange request not found")
        
        # Only skill owner can update the request status
        if request.skill_owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this request status")
        
        # Update the status
        updated_request = update_skill_exchange_request_status(db, request_id=request_id, status=new_status)
        
        if not updated_request:
            raise HTTPException(status_code=500, detail="Failed to update request status")
        
        return {
            "message": f"Request status updated to {new_status}",
            "request_id": request_id,
            "status": new_status,
            "updated_at": updated_request.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Failed to update request status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
