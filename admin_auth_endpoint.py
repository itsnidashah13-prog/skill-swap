"""
Admin Authentication Endpoint for Backend
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel

from database import get_db, Settings
from crud import get_user_by_username, verify_password
from schemas import UserCreate

# Settings instance
settings = Settings()

# Create admin auth router
admin_auth_router = APIRouter(prefix="/admin", tags=["admin-auth"])

# Use APIKeyHeader for Authorization header
api_key_header = APIKeyHeader(
    name="Authorization",
    scheme_name="JWTAuth",
    description="**Enter your JWT token** (copy the access_token from login response, paste it here WITH 'Bearer ' prefix: Bearer your_token_here)",
    auto_error=False
)

# Pydantic model for login request
class AdminLoginRequest(BaseModel):
    username: str
    password: str

@admin_auth_router.post("/login")
async def admin_login(login_data: AdminLoginRequest, db: Session = Depends(get_db)):
    """Admin login endpoint that returns JWT token"""
    
    username = login_data.username
    password = login_data.password
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required"
        )
    
    # Try to find user by username or email
    user = get_user_by_username(db, username)
    if not user:
        # Try to find by email if username not found
        from crud import get_user_by_email
        user = get_user_by_email(db, username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is admin (username is 'admin' or email contains 'admin')
    if user.username != 'admin' and 'admin' not in user.email.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required.",
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=60)
    expire = datetime.utcnow() + access_token_expires
    
    to_encode = {
        "sub": user.username,
        "exp": expire,
        "role": "admin",
        "is_admin": True,
        "user_id": user.id
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return JSONResponse({
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "expires_in": 3600,
        "admin_user": {
            "username": user.username,
            "email": user.email,
            "role": "admin",
            "is_admin": True,
            "user_id": user.id
        }
    })

@admin_auth_router.post("/token")
async def admin_token(login_data: AdminLoginRequest, db: Session = Depends(get_db)):
    """Alternative admin token endpoint"""
    return await admin_login(login_data, db)

@admin_auth_router.get("/verify")
async def verify_admin_token(authorization: str = Depends(api_key_header)):
    """Verify admin token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required with Bearer token"
        )
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        
        if is_admin:
            return JSONResponse({
                "valid": True,
                "username": username,
                "role": "admin",
                "is_admin": True,
                "expires": payload.get("exp")
            })
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin token"
            )
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token"
        )
