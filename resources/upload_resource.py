from fastapi import APIRouter, Depends, Query, HTTPException, Form
from utils.auth import verify_token
import requests
import os
from models.upload import VideoUpload

router = APIRouter()

UPLOAD_SERVICE_URL = os.getenv("UPLOAD_SERVICE_URL")

@router.post("/videos/start_upload")
async def upload_video(
    # file: UploadFile,
    uploadBody: VideoUpload
):
    """
    Composite layer Upload endpoint.
    request forwarded to Upload Microservice.
    """

    if not UPLOAD_SERVICE_URL:
        raise HTTPException(status_code=500, detail="UPLOAD_SERVICE_URL not set")

    body = {
        "offering_id": uploadBody.offering_id,
        "prof_uni": uploadBody.prof_uni,
        "videoTitle": uploadBody.videoTitle,
    }
    try:
        # Call Search Microservice
        res = requests.post(
            f"{UPLOAD_SERVICE_URL}/videos/start_upload",
            json=body,
            timeout=5
        )

        
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Upload microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Upload microservice unavailable")
