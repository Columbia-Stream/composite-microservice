# dbservice/resources/video_resource.py
from fastapi import APIRouter, Depends, Query
from typing import List
from utils.auth import verify_token
from services.video_service import search_videos
from models.video import Video

router = APIRouter()

@router.get("/videos/search", response_model=List[Video])
def search_videos_route(
    q: str = Query(None),
    offering_id: str = Query(None),
    prof: str = Query(None),
    limit: int = Query(20),
    user=Depends(verify_token) 
):
    print(f"[DEBUG] User verified: {user}")
    return search_videos(q, offering_id, prof, limit)
