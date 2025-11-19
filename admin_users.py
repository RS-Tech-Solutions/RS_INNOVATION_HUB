from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from datetime import datetime
from ..server import (
    db, User, UserResponse, UserRole, get_current_user, require_role
)

router = APIRouter(prefix="/api/admin", tags=["Admin - User Management"])

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: dict = Depends(require_role(UserRole.MANAGER)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role_filter: UserRole = None,
    is_active: bool = None
):
    filter_dict = {}
    if role_filter:
        filter_dict["role"] = role_filter
    if is_active is not None:
        filter_dict["is_active"] = is_active
    
    users = await db.users.find(filter_dict, {"password": 0}).skip(skip).limit(limit).to_list(limit)
    return [UserResponse(**user) for user in users]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_details(
    user_id: str,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    user = await db.users.find_one({"id": user_id}, {"password": 0})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_data: dict,
    current_user: dict = Depends(require_role(UserRole.OWNER))
):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_role = role_data.get("role")
    if new_role not in [role.value for role in UserRole]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    # Prevent changing own role
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    # Only owners can create other owners
    if new_role == UserRole.OWNER and current_user["role"] != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can assign owner role"
        )
    
    await db.users.update_one(
        {"id": user_id},
        {"$set": {"role": new_role, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": f"User role updated to {new_role}"}

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    status_data: dict,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deactivating own account
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Only owners can deactivate other owners
    if user["role"] == UserRole.OWNER and current_user["role"] != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can deactivate other owners"
        )
    
    is_active = status_data.get("is_active", True)
    
    await db.users.update_one(
        {"id": user_id},
        {"$set": {"is_active": is_active, "updated_at": datetime.utcnow()}}
    )
    
    action = "activated" if is_active else "deactivated"
    return {"message": f"User {action} successfully"}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_role(UserRole.OWNER))
):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting own account
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    await db.users.delete_one({"id": user_id})
    return {"message": "User deleted successfully"}