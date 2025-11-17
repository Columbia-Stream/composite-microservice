from fastapi import APIRouter, Depends, Query, HTTPException
from utils.auth import verify_token
import requests
import os

router = APIRouter()

SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL")


@router.get("/videos/search")
def search_videos_proxy(
    q: str = Query(None),
    course_id: str = Query(None),          # support course_id
    offering_id: int = Query(None),        # optional, if needed
    prof: str = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user=Depends(verify_token)
):
    """
    Composite layer search endpoint.
    Auth validated here, then request forwarded to Search Microservice.
    Supports q, course_id, offering_id, prof, limit, offset.
    """

    if not SEARCH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="SEARCH_SERVICE_URL not set")

    # Build outbound params
    params = {
        "q": q,
        "course_id": course_id,
        "offering_id": offering_id,
        "prof": prof,
        "limit": limit,
        "offset": offset
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        # Call Search Microservice
        res = requests.get(
            f"{SEARCH_SERVICE_URL}/search/videos",
            params=params,
            headers={"Authorization": f"Bearer {user['token']}"},
            timeout=5
        )

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        data = res.json()

        # Normalize structure into flattened form
        if isinstance(data, dict) and "items" in data:
            flattened = {
                "items": data.get("items", []),
                "page_size": data.get("page_size"),
                "offset": data.get("offset"),
                "links": data.get("links", []),
            }
        else:
            # Fallback (raw list)
            flattened = {"items": data, "links": []}

        # Add self link
        flattened["links"].append({
            "rel": "self",
            "href": (
                f"/videos/search?"
                f"q={q or ''}&"
                f"course_id={course_id or ''}&"
                f"offering_id={offering_id or ''}&"
                f"prof={prof or ''}&"
                f"limit={limit}&offset={offset}"
            )
        })

        return flattened

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Search microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Search microservice unavailable")
