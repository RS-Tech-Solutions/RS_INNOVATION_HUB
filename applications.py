from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..server import (
    db, Application, ApplicationCreate, ApplicationStatus, ApplicationType,
    get_current_user, require_role, UserRole
)

router = APIRouter(prefix="/api", tags=["Applications"])

# User endpoint - submit application
@router.post("/applications", response_model=Application)
async def submit_application(
    app_data: ApplicationCreate,
    current_user: dict = Depends(get_current_user)
):
    # Validate that either program_id or event_id is provided
    if app_data.type == ApplicationType.PROGRAM and not app_data.program_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="program_id is required for program applications"
        )
    
    if app_data.type == ApplicationType.EVENT and not app_data.event_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="event_id is required for event applications"
        )
    
    # Check if user has already applied
    existing_app = None
    if app_data.program_id:
        existing_app = await db.applications.find_one({
            "user_id": current_user["id"],
            "program_id": app_data.program_id
        })
    elif app_data.event_id:
        existing_app = await db.applications.find_one({
            "user_id": current_user["id"],
            "event_id": app_data.event_id
        })
    
    if existing_app:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this program/event"
        )
    
    # Create application
    application = Application(
        user_id=current_user["id"],
        **app_data.dict()
    )
    
    await db.applications.insert_one(application.dict())
    
    # Update participant count if it's an event
    if app_data.event_id:
        await db.events.update_one(
            {"id": app_data.event_id},
            {"$inc": {"current_registrations": 1}}
        )
    elif app_data.program_id:
        await db.programs.update_one(
            {"id": app_data.program_id},
            {"$inc": {"current_participants": 1}}
        )
    
    return application

# User endpoint - get user's applications
@router.get("/applications/my", response_model=List[Application])
async def get_my_applications(
    current_user: dict = Depends(get_current_user)
):
    applications = await db.applications.find({"user_id": current_user["id"]}).to_list(1000)
    return [Application(**app) for app in applications]

# Admin endpoints
@router.get("/admin/applications", response_model=List[dict])
async def get_all_applications(
    current_user: dict = Depends(require_role(UserRole.EDITOR)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[ApplicationStatus] = None,
    type_filter: Optional[ApplicationType] = None
):
    filter_dict = {}
    if status_filter:
        filter_dict["status"] = status_filter
    if type_filter:
        filter_dict["type"] = type_filter
    
    applications = await db.applications.find(filter_dict).skip(skip).limit(limit).to_list(limit)
    
    # Enrich with user, program, and event data
    enriched_applications = []
    for app in applications:
        # Get user data
        user = await db.users.find_one({"id": app["user_id"]})
        app["user"] = {"name": user["name"], "email": user["email"]} if user else None
        
        # Get program/event data
        if app.get("program_id"):
            program = await db.programs.find_one({"id": app["program_id"]})
            app["program"] = {"title": program["title"]} if program else None
        
        if app.get("event_id"):
            event = await db.events.find_one({"id": app["event_id"]})
            app["event"] = {"title": event["title"]} if event else None
        
        enriched_applications.append(app)
    
    return enriched_applications

@router.get("/admin/applications/{application_id}", response_model=dict)
async def get_application_details(
    application_id: str,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    application = await db.applications.find_one({"id": application_id})
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Enrich with user data
    user = await db.users.find_one({"id": application["user_id"]})
    application["user"] = user
    
    # Get program/event data
    if application.get("program_id"):
        program = await db.programs.find_one({"id": application["program_id"]})
        application["program"] = program
    
    if application.get("event_id"):
        event = await db.events.find_one({"id": application["event_id"]})
        application["event"] = event
    
    return application

@router.put("/admin/applications/{application_id}/status")
async def update_application_status(
    application_id: str,
    status_data: dict,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    application = await db.applications.find_one({"id": application_id})
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    new_status = status_data.get("status")
    review_notes = status_data.get("review_notes", "")
    
    if new_status not in [status.value for status in ApplicationStatus]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    update_data = {
        "status": new_status,
        "review_notes": review_notes,
        "reviewed_by": current_user["id"],
        "reviewed_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.applications.update_one(
        {"id": application_id},
        {"$set": update_data}
    )
    
    return {"message": "Application status updated successfully"}

@router.delete("/admin/applications/{application_id}")
async def delete_application(
    application_id: str,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    application = await db.applications.find_one({"id": application_id})
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    await db.applications.delete_one({"id": application_id})
    return {"message": "Application deleted successfully"}