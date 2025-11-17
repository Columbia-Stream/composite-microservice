# composite/resources/video_resource.py
from fastapi import APIRouter, Depends, Query, HTTPException
from utils.auth import verify_token
import requests
import os

router = APIRouter()

SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL")

@router.get("/videos/search")
def search_videos_proxy(
    q: str = Query(None),
    offering_id: int = Query(None),
    prof: str = Query(None),
    limit: int = Query(20),
    user=Depends(verify_token)
):
    """
    Delegates to the Search microservice after verifying auth.
    """
    if not SEARCH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="SEARCH_SERVICE_URL not set")

    try:
        # Forward query params to Search microservice
        params = {
            "q": q,
            "offering_id": offering_id,
            "prof": prof,
            "limit": limit
        }
        # Filter out None values so the URL is clean
        params = {k: v for k, v in params.items() if v is not None}

        res = requests.get(
            f"{SEARCH_SERVICE_URL}/search/videos",
            params=params,
            headers={"Authorization": f"Bearer {user['token']}"},
            timeout=5
        )

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        data = res.json()
        # Add relative link data if you want to meet “linked data” requirement
        if isinstance(data, dict) and "items" in data:
            # Merge top-level fields from Search (items, pagination, links)
            flattened = {
                "items": data.get("items", []),
                "page_size": data.get("page_size"),
                "offset": data.get("offset"),
                "links": data.get("links", []),
            }
        else:
            # If Search ever returns a raw list (fallback)
            flattened = {"items": data, "links": []}

        # Add composite-level link for relative reference
        flattened["links"].append(
            {"rel": "self", "href": f"/videos/search?q={q or ''}&limit={limit}"}
        )

        return flattened

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Search microservice timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Search microservice unavailable")