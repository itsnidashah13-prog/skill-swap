from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from jose.exceptions import JWTError as JoseJWTError
from database import get_db, settings
from models import User
from schemas import UserCreate, UserResponse, UserLogin, Token, UserUpdate
from crud import create_user, get_user, get_user_by_username, get_user_by_email, authenticate_user, update_user

router = APIRouter(tags=["users"])

# Configure API key authentication for Swagger UI
from fastapi.security import APIKeyHeader

# Use APIKeyHeader instead of OAuth2PasswordBearer for better Swagger integration
api_key_header = APIKeyHeader(
    name="Authorization",
    scheme_name="JWTAuth",
    description="**Enter your JWT token** (copy the access_token from login response, paste it here WITH 'Bearer ' prefix: Bearer your_token_here)",
    auto_error=False
)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def get_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    """
    Get current authenticated user from JWT token.
    
    Args:
        authorization: Authorization header with Bearer token
        db: Database session
        
    Returns:
        User object if authentication successful
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please check your token and try again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f" DEBUG: Authorization header received: {authorization[:50]}..." if authorization and len(authorization) > 50 else f" DEBUG: Authorization header: {authorization}")
    
    if not authorization:
        print(" DEBUG: No authorization header provided")
        raise credentials_exception
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            print(f" DEBUG: Invalid scheme: {scheme}, expected 'bearer'")
            raise credentials_exception
    except ValueError:
        print(f" DEBUG: Invalid authorization format: {authorization}")
        raise credentials_exception
    
    print(f" DEBUG: Extracted token: {token[:20]}...")
    print(f" DEBUG: Secret key: {settings.secret_key[:20]}...")
    print(f" DEBUG: Algorithm: {settings.algorithm}")
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except JoseJWTError as e:
        raise credentials_exception
    except Exception as e:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active"
        )
    
    return user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return create_user(db=db, user=user)

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_info(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    db_user = update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
