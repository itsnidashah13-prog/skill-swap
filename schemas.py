from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Skill schemas
class SkillBase(BaseModel):
    title: str
    description: str
    category: str
    proficiency_level: str
    value: Optional[int] = None  # New value feature - skill value/experience points
    
    class Config:
        from_attributes = True
        # Example for Swagger documentation
        json_schema_extra = {
            "example": {
                "title": "Python Programming",
                "description": "Learn Python from basics to advanced concepts including OOP, data structures, and algorithms",
                "category": "Programming",
                "proficiency_level": "Advanced",
                "value": 100
            }
        }

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    proficiency_level: Optional[str] = None
    value: Optional[int] = None  # New value feature
    is_active: Optional[bool] = None

class SkillResponse(SkillBase):
    id: int
    user_id: int
    created_at: datetime
    is_active: bool
    owner: UserResponse
    
    class Config:
        from_attributes = True

# Notification schemas
class NotificationBase(BaseModel):
    title: str
    message: str
    type: str
    related_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Skill Exchange Request schemas
class SkillExchangeRequestBase(BaseModel):
    skill_id: int
    message: str

class SkillExchangeRequestCreate(SkillExchangeRequestBase):
    pass

class SkillExchangeRequestUpdate(BaseModel):
    status: str  # pending, accepted, rejected, completed

class SkillExchangeRequestResponse(SkillExchangeRequestBase):
    id: int
    requester_id: int
    skill_owner_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    skill: SkillResponse
    requester: UserResponse
    skill_owner: UserResponse
    
    class Config:
        from_attributes = True
