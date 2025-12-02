from fastapi import APIRouter, Depends, Query, HTTPException
from utils.auth import verify_token
import requests
import os

router = APIRouter()

SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL")
VIDEO_COMPOSITE_URL = os.getenv("VIDEO_COMPOSITE_URL")

# ---------------------------------------------------------
# 1. SEARCH ENDPOINT
# ---------------------------------------------------------
@router.get("/videos/search")
def search_videos_proxy(
    q: str = Query(None),
    course_id: str = Query(None),
    offering_id: int = Query(None),
    prof: str = Query(None),
    year: int = Query(None),            # NEW
    semester: str = Query(None),        # NEW
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user=Depends(verify_token)
):
    """
    Composite layer search endpoint.
    Supports q, course_id, offering_id, prof, year, semester, limit, offset.
    """

    if not SEARCH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="SEARCH_SERVICE_URL not set")

    # Build downstream params
    params = {
        "q": q,
        "course_id": course_id,
        "offering_id": offering_id,
        "prof": prof,
        "year": year,            # NEW
        "semester": semester,    # NEW
        "limit": limit,
        "offset": offset,
    }

    # Drop None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        res = requests.get(
            f"{SEARCH_SERVICE_URL}/search/videos",
            params=params,
            headers={"Authorization": f"Bearer {user['token']}"},
            timeout=5
        )

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        data = res.json()

        # Normalize output
        if isinstance(data, dict) and "items" in data:
            flattened = {
                "items": data.get("items", []),
                "page_size": data.get("page_size"),
                "offset": data.get("offset"),
                "links": data.get("links", []),
            }
        else:
            flattened = {"items": data, "links": []}

        flattened["links"].append({
            "rel": "self",
            "href": (
                f"/videos/search?"
                f"q={q or ''}&"
                f"course_id={course_id or ''}&"
                f"offering_id={offering_id or ''}&"
                f"prof={prof or ''}&"
                f"year={year or ''}&"
                f"semester={semester or ''}&"
                f"limit={limit}&offset={offset}"
            )
        })

        return flattened

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Search microservice timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Search microservice unavailable")


# ---------------------------------------------------------
# 2. GET SINGLE VIDEO METADATA
# ---------------------------------------------------------
@router.get("/videos/{video_id}")
def get_single_video(video_id: str, user=Depends(verify_token)):
    """
    Fetch metadata for a single video.
    """

    if not VIDEO_COMPOSITE_URL:
        raise HTTPException(status_code=500, detail="VIDEO_COMPOSITE_URL not set")

    try:
        res = requests.get(
            f"{VIDEO_COMPOSITE_URL}/videos/{video_id}",
            headers={"Authorization": f"Bearer {user['token']}"},
            timeout=5,
        )

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Video composite timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Video composite unavailable")
