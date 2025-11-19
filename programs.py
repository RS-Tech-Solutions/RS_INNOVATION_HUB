from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from server import (
    db, Program, ProgramCreate, ProgramCategory, get_current_user, require_role, UserRole
)
router = APIRouter(prefix="/api", tags=["Programs"])

# Public endpoint - get all active programs
@router.get("/programs", response_model=List[Program])
async def get_programs(
    category: Optional[ProgramCategory] = None,
    is_active: bool = True
):
    filter_dict = {"is_active": is_active} if is_active else {}
    if category:
        filter_dict["category"] = category
    
    programs = await db.programs.find(filter_dict).to_list(1000)
    return [Program(**program) for program in programs]

# Public endpoint - get single program
@router.get("/programs/{program_id}", response_model=Program)
async def get_program(program_id: str):
    program = await db.programs.find_one({"id": program_id, "is_active": True})
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    return Program(**program)

# Admin endpoints
@router.post("/admin/programs", response_model=Program)
async def create_program(
    program_data: ProgramCreate,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    program = Program(
        **program_data.dict(),
        created_by=current_user["id"]
    )
    
    await db.programs.insert_one(program.dict())
    return program

@router.get("/admin/programs", response_model=List[Program])
async def get_all_programs_admin(
    current_user: dict = Depends(require_role(UserRole.EDITOR)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[ProgramCategory] = None,
    is_active: Optional[bool] = None
):
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if is_active is not None:
        filter_dict["is_active"] = is_active
    
    programs = await db.programs.find(filter_dict).skip(skip).limit(limit).to_list(limit)
    return [Program(**program) for program in programs]

@router.get("/admin/programs/{program_id}", response_model=Program)
async def get_program_admin(
    program_id: str,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    program = await db.programs.find_one({"id": program_id})
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    return Program(**program)

@router.put("/admin/programs/{program_id}", response_model=Program)
async def update_program(
    program_id: str,
    program_data: ProgramCreate,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    program = await db.programs.find_one({"id": program_id})
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    update_data = program_data.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.programs.update_one(
        {"id": program_id},
        {"$set": update_data}
    )
    
    updated_program = await db.programs.find_one({"id": program_id})
    return Program(**updated_program)

@router.delete("/admin/programs/{program_id}")
async def delete_program(
    program_id: str,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    program = await db.programs.find_one({"id": program_id})
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    # Soft delete - just set is_active to False
    await db.programs.update_one(
        {"id": program_id},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Program deleted successfully"}