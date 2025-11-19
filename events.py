from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from server import (
    db, Event, EventCreate, EventStatus, get_current_user, require_role, UserRole
)

router = APIRouter(prefix="/api", tags=["Events"])

# Public endpoint - get all events
@router.get("/events", response_model=List[Event])
async def get_events(status_filter: Optional[EventStatus] = None):
    filter_dict = {}
    if status_filter:
        filter_dict["status"] = status_filter
    
    events = await db.events.find(filter_dict).to_list(1000)
    return [Event(**event) for event in events]

# Public endpoint - get single event
@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str):
    event = await db.events.find_one({"id": event_id})
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return Event(**event)

# Admin endpoints
@router.post("/admin/events", response_model=Event)
async def create_event(
    event_data: EventCreate,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    event = Event(
        **event_data.dict(),
        created_by=current_user["id"]
    )
    
    await db.events.insert_one(event.dict())
    return event

@router.get("/admin/events", response_model=List[Event])
async def get_all_events_admin(
    current_user: dict = Depends(require_role(UserRole.EDITOR)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[EventStatus] = None
):
    filter_dict = {}
    if status_filter:
        filter_dict["status"] = status_filter
    
    events = await db.events.find(filter_dict).skip(skip).limit(limit).to_list(limit)
    return [Event(**event) for event in events]

@router.get("/admin/events/{event_id}", response_model=Event)
async def get_event_admin(
    event_id: str,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    event = await db.events.find_one({"id": event_id})
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return Event(**event)

@router.put("/admin/events/{event_id}", response_model=Event)
async def update_event(
    event_id: str,
    event_data: EventCreate,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    event = await db.events.find_one({"id": event_id})
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event_data.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.events.update_one(
        {"id": event_id},
        {"$set": update_data}
    )
    
    updated_event = await db.events.find_one({"id": event_id})
    return Event(**updated_event)

@router.delete("/admin/events/{event_id}")
async def delete_event(
    event_id: str,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    event = await db.events.find_one({"id": event_id})
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    await db.events.delete_one({"id": event_id})
    return {"message": "Event deleted successfully"}