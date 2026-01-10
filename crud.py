from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from models import User, Skill, SkillExchangeRequest, Notification
from schemas import UserCreate, UserUpdate, SkillCreate, SkillUpdate, SkillExchangeRequestCreate, SkillExchangeRequestUpdate, NotificationCreate
import bcrypt
from typing import Optional, List
from datetime import datetime

# Password hashing functions
def hash_password(password: str) -> str:
    # Truncate password to 72 characters max for bcrypt
    truncated_password = password[:72] if len(password) > 72 else password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(truncated_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    return bcrypt.checkpw(truncated_password.encode('utf-8'), hashed_password.encode('utf-8'))

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.is_active == True).order_by(User.created_at.desc()).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        bio=user.bio,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

# Skill CRUD operations
def get_skill(db: Session, skill_id: int):
    return db.query(Skill).options(joinedload(Skill.owner)).filter(Skill.id == skill_id).first()

def get_skills(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None):
    query = db.query(Skill).options(joinedload(Skill.owner)).filter(Skill.is_active == True).order_by(Skill.created_at.desc())
    if category:
        query = query.filter(Skill.category == category)
    return query.offset(skip).limit(limit).all()

def get_skills_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Skill).options(joinedload(Skill.owner)).filter(and_(Skill.user_id == user_id, Skill.is_active == True)).order_by(Skill.created_at.desc()).offset(skip).limit(limit).all()

def create_skill(db: Session, skill: SkillCreate, user_id: int):
    db_skill = Skill(
        title=skill.title,
        description=skill.description,
        category=skill.category,
        proficiency_level=skill.proficiency_level,
        value=skill.value,
        user_id=user_id
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def update_skill(db: Session, skill_id: int, skill_update: SkillUpdate):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill:
        update_data = skill_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_skill, field, value)
        db.commit()
        db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: int):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill:
        db_skill.is_active = False
        db.commit()
        db.refresh(db_skill)
    return db_skill

# Skill Exchange Request CRUD operations
def get_skill_exchange_request(db: Session, request_id: int):
    return db.query(SkillExchangeRequest).filter(SkillExchangeRequest.id == request_id).first()

def get_skill_exchange_requests(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    try:
        query = db.query(SkillExchangeRequest).order_by(SkillExchangeRequest.created_at.desc())
        
        # Load relationships separately to avoid complex joins
        requests = query.offset(skip).limit(limit).all()
        
        # Manually load relationships
        result = []
        for request in requests:
            # Load requester
            requester = db.query(User).filter(User.id == request.requester_id).first()
            # Load skill and owner
            skill = db.query(Skill).filter(Skill.id == request.skill_id).first()
            skill_owner = db.query(User).filter(User.id == request.skill_owner_id).first()
            
            # Create response dict
            request_dict = {
                'id': request.id,
                'skill_id': request.skill_id,
                'requester_id': request.requester_id,
                'skill_owner_id': request.skill_owner_id,
                'message': request.message,
                'status': request.status,
                'created_at': request.created_at.isoformat() if request.created_at else None,
                'updated_at': request.updated_at.isoformat() if request.updated_at else None,
                'requester': {
                    'id': requester.id,
                    'username': requester.username,
                    'email': requester.email,
                    'full_name': requester.full_name
                } if requester else None,
                'skill': {
                    'id': skill.id,
                    'title': skill.title,
                    'category': skill.category,
                    'proficiency_level': skill.proficiency_level
                } if skill else None,
                'skill_owner': {
                    'id': skill_owner.id,
                    'username': skill_owner.username,
                    'email': skill_owner.email,
                    'full_name': skill_owner.full_name
                } if skill_owner else None
            }
            result.append(request_dict)
        
        return result
    except Exception as e:
        print(f"Error in get_skill_exchange_requests: {e}")
        # Return empty list as fallback
        return []

def get_skill_exchange_requests_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    try:
        # Get requests sent by user and requests for user's skills
        query = db.query(SkillExchangeRequest).filter(
            and_(
                or_(
                    SkillExchangeRequest.requester_id == user_id,
                    SkillExchangeRequest.skill_owner_id == user_id
                )
            )
        ).order_by(SkillExchangeRequest.created_at.desc())
        
        requests = query.offset(skip).limit(limit).all()
        
        # Manually load relationships
        result = []
        for request in requests:
            # Load requester
            requester = db.query(User).filter(User.id == request.requester_id).first()
            # Load skill and owner
            skill = db.query(Skill).filter(Skill.id == request.skill_id).first()
            skill_owner = db.query(User).filter(User.id == request.skill_owner_id).first()
            
            # Create response dict
            request_dict = {
                'id': request.id,
                'skill_id': request.skill_id,
                'requester_id': request.requester_id,
                'skill_owner_id': request.skill_owner_id,
                'message': request.message,
                'status': request.status,
                'created_at': request.created_at.isoformat() if request.created_at else None,
                'updated_at': request.updated_at.isoformat() if request.updated_at else None,
                'requester': {
                    'id': requester.id,
                    'username': requester.username,
                    'email': requester.email,
                    'full_name': requester.full_name
                } if requester else None,
                'skill': {
                    'id': skill.id,
                    'title': skill.title,
                    'category': skill.category,
                    'proficiency_level': skill.proficiency_level
                } if skill else None,
                'skill_owner': {
                    'id': skill_owner.id,
                    'username': skill_owner.username,
                    'email': skill_owner.email,
                    'full_name': skill_owner.full_name
                } if skill_owner else None
            }
            result.append(request_dict)
        
        return result
    except Exception as e:
        print(f"Error in get_skill_exchange_requests_for_user: {e}")
        # Return empty list as fallback
        return []

def create_skill_exchange_request(db: Session, request: SkillExchangeRequestCreate, requester_id: int, skill_owner_id: int):
    try:
        print(f"DEBUG: Creating skill exchange request with data:")
        print(f"  - skill_id: {request.skill_id}")
        print(f"  - message: {request.message}")
        print(f"  - requester_id: {requester_id}")
        print(f"  - skill_owner_id: {skill_owner_id}")
        
        db_request = SkillExchangeRequest(
            skill_id=request.skill_id,
            message=request.message,
            requester_id=requester_id,
            skill_owner_id=skill_owner_id
        )
        
        print(f"DEBUG: Adding request to database...")
        db.add(db_request)
        
        print(f"DEBUG: Committing to database...")
        db.commit()
        
        print(f"DEBUG: Refreshing request object...")
        db.refresh(db_request)
        
        print(f"DEBUG: Skill exchange request created successfully with ID: {db_request.id}")
        return db_request
        
    except Exception as e:
        print(f"ERROR: Failed to create skill exchange request: {e}")
        print(f"ERROR: Exception type: {type(e).__name__}")
        print(f"ERROR: Exception details: {str(e)}")
        # Re-raise the exception so it shows up in the API response
        raise e

def update_skill_exchange_request_status(db: Session, request_id: int, status: str):
    """Update the status of a skill exchange request"""
    try:
        print(f"DEBUG: Updating request {request_id} status to '{status}'")
        
        # Get the request
        request = db.query(SkillExchangeRequest).filter(SkillExchangeRequest.id == request_id).first()
        
        if not request:
            print(f"ERROR: Request {request_id} not found")
            return None
        
        # Update status
        request.status = status
        request.updated_at = datetime.utcnow()
        
        print(f"DEBUG: Committing status update...")
        db.commit()
        db.refresh(request)
        
        print(f"DEBUG: Request {request_id} status updated to '{status}'")
        return request
        
    except Exception as e:
        print(f"ERROR: Failed to update request status: {e}")
        print(f"ERROR: Exception type: {type(e).__name__}")
        print(f"ERROR: Exception details: {str(e)}")
        raise e

def update_skill_exchange_request(db: Session, request_id: int, request_update: SkillExchangeRequestUpdate):
    db_request = db.query(SkillExchangeRequest).filter(SkillExchangeRequest.id == request_id).first()
    if db_request:
        update_data = request_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_request, field, value)
        db.commit()
        db.refresh(db_request)
    return db_request

# Notification CRUD operations
def create_notification(db: Session, notification: NotificationCreate):
    db_notification = Notification(
        title=notification.title,
        message=notification.message,
        type=notification.type,
        related_id=notification.related_id,
        user_id=notification.user_id
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

def mark_notification_read(db: Session, notification_id: int, user_id: int):
    db_notification = db.query(Notification).filter(
        and_(Notification.id == notification_id, Notification.user_id == user_id)
    ).first()
    if db_notification:
        db_notification.is_read = True
        db.commit()
        db.refresh(db_notification)
    return db_notification

def get_unread_notification_count(db: Session, user_id: int):
    return db.query(Notification).filter(
        and_(Notification.user_id == user_id, Notification.is_read == False)
    ).count()
