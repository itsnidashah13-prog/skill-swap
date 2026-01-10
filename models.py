from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    skills_offered = relationship("Skill", foreign_keys="Skill.user_id", back_populates="owner")
    skill_requests_sent = relationship("SkillExchangeRequest", foreign_keys="SkillExchangeRequest.requester_id", back_populates="requester")
    skill_requests_received = relationship("SkillExchangeRequest", foreign_keys="SkillExchangeRequest.skill_owner_id", back_populates="skill_owner")
    notifications = relationship("Notification", back_populates="user")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    proficiency_level = Column(String(20), nullable=False)  # Beginner, Intermediate, Advanced, Expert
    value = Column(Integer, default=0)  # New value feature - skill value/experience points
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    owner = relationship("User", foreign_keys=[user_id], back_populates="skills_offered")
    exchange_requests = relationship("SkillExchangeRequest", back_populates="skill")

class SkillExchangeRequest(Base):
    __tablename__ = "skill_exchange_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, rejected, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    skill = relationship("Skill", back_populates="exchange_requests")
    requester = relationship("User", foreign_keys=[requester_id], back_populates="skill_requests_sent")
    skill_owner = relationship("User", foreign_keys=[skill_owner_id], back_populates="skill_requests_received")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # swap_request, swap_accepted, swap_rejected
    related_id = Column(Integer, nullable=True)  # ID of related object (e.g., request_id)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
