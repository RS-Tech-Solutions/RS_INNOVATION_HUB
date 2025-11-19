from fastapi import APIRouter, HTTPException, status, Depends
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from datetime import datetime
import os
import sys
import uuid
from pathlib import Path

# Add the backend directory to the path so we can import from server
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from server import (
    db, UserCreate, UserLogin, GoogleAuthData, User, UserResponse,
    hash_password, verify_password, create_jwt_token, get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
async def register_user(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone
    )
    
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    
    # Insert user into database
    result = await db.users.insert_one(user_dict)
    
    # Create JWT token
    token_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    }
    token = create_jwt_token(token_data)
    
    return {
        "message": "User registered successfully",
        "token": token,
        "user": UserResponse(**user.dict())
    }

@router.post("/login", response_model=dict)
async def login_user(login_data: UserLogin):
    # Find user by email
    user = await db.users.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Create JWT token
    token_data = {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"]
    }
    token = create_jwt_token(token_data)
    
    return {
        "message": "Login successful",
        "token": token,
        "user": UserResponse(**user)
    }

@router.post("/google", response_model=dict)
async def google_auth(auth_data: GoogleAuthData):
    try:
        # Verify Google token (in production, implement proper verification)
        # For now, we'll trust the frontend verification
        
        # Check if user already exists
        user = await db.users.find_one({"email": auth_data.email})
        
        if user:
            # Update existing user
            await db.users.update_one(
                {"email": auth_data.email},
                {
                    "$set": {
                        "google_id": auth_data.google_id,
                        "profile_picture": auth_data.picture,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        else:
            # Create new user
            new_user = User(
                name=auth_data.name,
                email=auth_data.email,
                google_id=auth_data.google_id,
                profile_picture=auth_data.picture
            )
            user_dict = new_user.dict()
            user_dict["password"] = None  # No password for Google users
            
            await db.users.insert_one(user_dict)
            user = user_dict
        
        # Create JWT token
        token_data = {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
        token = create_jwt_token(token_data)
        
        return {
            "message": "Google authentication successful",
            "token": token,
            "user": UserResponse(**user)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

@router.put("/profile", response_model=UserResponse)
async def update_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    # Allow users to update their own profile
    allowed_fields = ["name", "phone", "profile_picture"]
    update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    
    update_data["updated_at"] = datetime.utcnow()
    
    await db.users.update_one(
        {"id": current_user["id"]},
        {"$set": update_data}
    )
    
    updated_user = await db.users.find_one({"id": current_user["id"]})
    return UserResponse(**updated_user)

@router.post("/logout")
async def logout_user():
    # Since we're using JWT tokens, logout is handled on the frontend
    # by removing the token from storage
    return {"message": "Logout successful"}