from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..server import (
    db, SuccessStory, SuccessStoryCreate, get_current_user, require_role, UserRole
)

router = APIRouter(prefix="/api", tags=["Success Stories"])

# Public endpoint - get published success stories
@router.get("/success-stories", response_model=List[SuccessStory])
async def get_success_stories():
    stories = await db.success_stories.find({"is_published": True}).to_list(1000)
    return [SuccessStory(**story) for story in stories]

# Public endpoint - get single success story
@router.get("/success-stories/{story_id}", response_model=SuccessStory)
async def get_success_story(story_id: str):
    story = await db.success_stories.find_one({"id": story_id, "is_published": True})
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Success story not found"
        )
    return SuccessStory(**story)

# Admin endpoints
@router.post("/admin/success-stories", response_model=SuccessStory)
async def create_success_story(
    story_data: SuccessStoryCreate,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    story = SuccessStory(
        **story_data.dict(),
        created_by=current_user["id"]
    )
    
    await db.success_stories.insert_one(story.dict())
    return story

@router.get("/admin/success-stories", response_model=List[SuccessStory])
async def get_all_success_stories_admin(
    current_user: dict = Depends(require_role(UserRole.EDITOR)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_published: Optional[bool] = None
):
    filter_dict = {}
    if is_published is not None:
        filter_dict["is_published"] = is_published
    
    stories = await db.success_stories.find(filter_dict).skip(skip).limit(limit).to_list(limit)
    return [SuccessStory(**story) for story in stories]

@router.get("/admin/success-stories/{story_id}", response_model=SuccessStory)
async def get_success_story_admin(
    story_id: str,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    story = await db.success_stories.find_one({"id": story_id})
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Success story not found"
        )
    return SuccessStory(**story)

@router.put("/admin/success-stories/{story_id}", response_model=SuccessStory)
async def update_success_story(
    story_id: str,
    story_data: SuccessStoryCreate,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    story = await db.success_stories.find_one({"id": story_id})
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Success story not found"
        )
    
    update_data = story_data.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.success_stories.update_one(
        {"id": story_id},
        {"$set": update_data}
    )
    
    updated_story = await db.success_stories.find_one({"id": story_id})
    return SuccessStory(**updated_story)

@router.put("/admin/success-stories/{story_id}/publish")
async def toggle_story_publication(
    story_id: str,
    publish_data: dict,
    current_user: dict = Depends(require_role(UserRole.EDITOR))
):
    story = await db.success_stories.find_one({"id": story_id})
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Success story not found"
        )
    
    is_published = publish_data.get("is_published", not story["is_published"])
    
    await db.success_stories.update_one(
        {"id": story_id},
        {"$set": {"is_published": is_published, "updated_at": datetime.utcnow()}}
    )
    
    action = "published" if is_published else "unpublished"
    return {"message": f"Success story {action} successfully"}

@router.delete("/admin/success-stories/{story_id}")
async def delete_success_story(
    story_id: str,
    current_user: dict = Depends(require_role(UserRole.MANAGER))
):
    story = await db.success_stories.find_one({"id": story_id})
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Success story not found"
        )
    
    await db.success_stories.delete_one({"id": story_id})
    return {"message": "Success story deleted successfully"}