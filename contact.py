from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..server import (
    db, Contact, ContactCreate, ContactStatus, get_current_user, require_role, UserRole
)

router = APIRouter(prefix="/api", tags=["Contact"])

# Public endpoint - submit contact form
@router.post("/contact", response_model=Contact)
async def submit_contact(
    contact_data: ContactCreate
):
    contact = Contact(**contact_data.dict())
    await db.contacts.insert_one(contact.dict())
    return contact

# Admin endpoints
@router.get("/admin/contacts", response_model=List[Contact])
async def get_all_contacts(
    current_user: dict = Depends(require_role(UserRole.EDITOR)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[ContactStatus] = None
):
    filter_dict = {}
    if status_filter:
        filter_dict["status"] = status_filter
    
    contacts = await db.contacts.find(filter_dict).skip(skip).limit(limit).to_list(limit)
    return [Contact(**contact) for contact in contacts]

@router.get("/admin/contacts/{contact_id}", response_model=Contact)
async def get_contact_details(
    contact_id: str,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    contact = await db.contacts.find_one({"id": contact_id})
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Mark as read if it's unread
    if contact["status"] == ContactStatus.UNREAD:
        await db.contacts.update_one(
            {"id": contact_id},
            {"$set": {"status": ContactStatus.read, "updated_at": datetime.utcnow()}}
        )
        contact["status"] = ContactStatus.read
    
    return Contact(**contact)

@router.put("/admin/contacts/{contact_id}/reply")
async def reply_to_contact(
    contact_id: str,
    reply_data: dict,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    contact = await db.contacts.find_one({"id": contact_id})
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    reply_message = reply_data.get("reply_message", "")
    if not reply_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reply message is required"
        )
    
    update_data = {
        "status": ContactStatus.REPLIED,
        "reply_message": reply_message,
        "replied_by": current_user["id"],
        "replied_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.contacts.update_one(
        {"id": contact_id},
        {"$set": update_data}
    )
    
    return {"message": "Reply sent successfully"}

@router.put("/admin/contacts/{contact_id}/status")
async def update_contact_status(
    contact_id: str,
    status_data: dict,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    contact = await db.contacts.find_one({"id": contact_id})
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    new_status = status_data.get("status")
    if new_status not in [status.value for status in ContactStatus]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    await db.contacts.update_one(
        {"id": contact_id},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Contact status updated successfully"}

@router.delete("/admin/contacts/{contact_id}")
async def delete_contact(
    contact_id: str,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    contact = await db.contacts.find_one({"id": contact_id})
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    await db.contacts.delete_one({"id": contact_id})
    return {"message": "Contact deleted successfully"}