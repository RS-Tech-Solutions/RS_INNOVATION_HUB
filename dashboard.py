from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from ..server import db, get_current_user, require_role, UserRole

router = APIRouter(prefix="/api/admin", tags=["Admin - Dashboard"])

@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    # Get total counts
    total_users = await db.users.count_documents({"is_active": True})
    total_programs = await db.programs.count_documents({"is_active": True})
    total_events = await db.events.count_documents({})
    total_applications = await db.applications.count_documents({})
    total_contacts = await db.contacts.count_documents({})
    total_success_stories = await db.success_stories.count_documents({"is_published": True})
    
    # Get recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    recent_users = await db.users.count_documents({
        "created_at": {"$gte": thirty_days_ago},
        "is_active": True
    })
    
    recent_applications = await db.applications.count_documents({
        "created_at": {"$gte": thirty_days_ago}
    })
    
    recent_contacts = await db.contacts.count_documents({
        "created_at": {"$gte": thirty_days_ago}
    })
    
    # Application status breakdown
    application_stats = await db.applications.aggregate([
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]).to_list(10)
    
    application_status_breakdown = {stat["_id"]: stat["count"] for stat in application_stats}
    
    # Contact status breakdown
    contact_stats = await db.contacts.aggregate([
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]).to_list(10)
    
    contact_status_breakdown = {stat["_id"]: stat["count"] for stat in contact_stats}
    
    # Program category breakdown
    program_stats = await db.programs.aggregate([
        {
            "$match": {"is_active": True}
        },
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }
        }
    ]).to_list(10)
    
    program_category_breakdown = {stat["_id"]: stat["count"] for stat in program_stats}
    
    # Recent applications with details
    recent_applications_detailed = await db.applications.find(
        {},
        {"form_data.name": 1, "type": 1, "status": 1, "created_at": 1}
    ).sort("created_at", -1).limit(5).to_list(5)
    
    # Recent contacts with details
    recent_contacts_detailed = await db.contacts.find(
        {},
        {"name": 1, "subject": 1, "status": 1, "created_at": 1}
    ).sort("created_at", -1).limit(5).to_list(5)
    
    return {
        "totals": {
            "users": total_users,
            "programs": total_programs,
            "events": total_events,
            "applications": total_applications,
            "contacts": total_contacts,
            "success_stories": total_success_stories
        },
        "recent_activity": {
            "new_users_30d": recent_users,
            "new_applications_30d": recent_applications,
            "new_contacts_30d": recent_contacts
        },
        "breakdowns": {
            "application_status": application_status_breakdown,
            "contact_status": contact_status_breakdown,
            "program_categories": program_category_breakdown
        },
        "recent_items": {
            "applications": recent_applications_detailed,
            "contacts": recent_contacts_detailed
        }
    }