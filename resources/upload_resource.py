from fastapi import APIRouter, Depends, Query, HTTPException, Form, status
# from utils.auth import verify_token
import requests
import os
from models.upload import VideoUpload

router = APIRouter()

UPLOAD_SERVICE_URL = os.getenv("UPLOAD_SERVICE_URL")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

@router.post("/start_upload")
async def upload_video(
    # file: UploadFile,
    uploadBody: VideoUpload
):
    """
    Composite layer Upload endpoint.
    request forwarded to Upload Microservice.
    """
    prof_uni = uploadBody.prof_uni
    offering_id = uploadBody.offering_id
    videoTitle = uploadBody.videoTitle
    if not UPLOAD_SERVICE_URL:
        raise HTTPException(status_code=500, detail="UPLOAD_SERVICE_URL not set")
    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")

    # Checking if user is in Users Table (FK constraint in Upload Microservice)
    bodyUni = {
        'uni': prof_uni
    }
    user_data = None

    try:
        auth_res = requests.get(
            f"{AUTH_SERVICE_URL}/auth/get-user",
            params=bodyUni,
            timeout=5
        )
        auth_res.raise_for_status()
        
        # 1b. Parse response into Pydantic Model for strict access
        user_data_wrapper = auth_res.json() # Renamed to avoid immediate collision

        # 1b. Validate the structure and content
        user_list = user_data_wrapper.get("user")

        # 1. Check if 'user' key is missing, or is not a list
        if not user_list or not isinstance(user_list, list):
            # This covers cases where the key might be missing, or the value is None/unexpected type
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Auth Service returned an invalid or missing 'user' list for UNI '{prof_uni}'. Response: {user_data_wrapper}"
            )

        # 2. Check if the 'user' list is empty (no result found)
        if len(user_list) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Professor UNI '{prof_uni}' not found in authentication system."
            )

        # 3. If all checks pass, assign the first element (the user object)
        # Assuming the query logic guarantees only one result per UNI
        user_data = user_list[0]
        # 2. AUTHORIZATION CHECK: Ensure the user is faculty
        if user_data.get('role') != 'faculty':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User '{prof_uni}' is registered as '{user_data.role}' and is not authorized to upload videos. Only 'faculty' users are allowed."
            )
        print(f"[DEBUG] Retrieved user data: {user_data}")
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Auth microservice timeout during user check.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Auth microservice unavailable.")
    except requests.exceptions.HTTPError as e:
        # User not found (404) or general Auth error
        if e.response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor UNI '{prof_uni}' not found in authentication system.")
        raise HTTPException(status_code=500, detail=f"Auth Service error: {e.response.text}")
    except Exception as e:
        # General JSON parsing error or unexpected failure
        raise HTTPException(status_code=500, detail=f"Internal error during user validation: {str(e)}")

    



    body = {
        "offering_id": offering_id,
        "prof_uni": prof_uni,
        "videoTitle": videoTitle,
    }
    try:
        # Call Search Microservice
        res = requests.post(
            f"{UPLOAD_SERVICE_URL}/videos/start_upload",
            json=body,
            timeout=5
        )
        print(f"[DEBUG] Upload response: {res.json()}")
        
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Upload microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Upload microservice unavailable")


@router.get("/offerings")
async def get_offerings():
    """
    Composite layer Upload endpoint.
    request forwarded to Upload Microservice.
    """

    if not UPLOAD_SERVICE_URL:
        raise HTTPException(status_code=500, detail="UPLOAD_SERVICE_URL not set")
    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")
    print(f"{UPLOAD_SERVICE_URL}/videos/offer")
    try:
        # Call Search Microservice
        res = requests.post(
            f"{UPLOAD_SERVICE_URL}/videos/offer",
            timeout=5
        )

        print(f"[DEBUG] Offerings response: {res.json()}")
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Upload microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Upload microservice unavailable")


@router.get("/courses")
async def get_courses():
    """
    Composite layer Upload endpoint.
    request forwarded to Upload Microservice.
    """

    if not UPLOAD_SERVICE_URL:
        raise HTTPException(status_code=500, detail="UPLOAD_SERVICE_URL not set")
    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")
    print(f"{UPLOAD_SERVICE_URL}/videos/courses")
    try:
        # Call Upload Microservice
        res = requests.post(
            f"{UPLOAD_SERVICE_URL}/videos/courses",
            timeout=5
        )

        print(f"[DEBUG] Courses response: {res.json()}")
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Upload microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Upload microservice unavailable")


@router.get("/prof_offer/{prof_uni}")
async def get_prof_offers(prof_uni: str):
    """
    Composite layer Upload endpoint.
    request forwarded to Upload Microservice.
    """

    if not UPLOAD_SERVICE_URL:
        raise HTTPException(status_code=500, detail="UPLOAD_SERVICE_URL not set")
    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")
    print(f"{UPLOAD_SERVICE_URL}/videos/prof_offer")
    try:
        # Call Upload Microservice
        res = requests.post(
            f"{UPLOAD_SERVICE_URL}/videos/prof_offer/{prof_uni}",
            timeout=5
        )

        print(f"[DEBUG] Prof Offers response: {res.json()}")
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Upload microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Upload microservice unavailable")
