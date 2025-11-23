from fastapi import APIRouter, Query, HTTPException
from utils.auth import verify_token
import requests
import os
import json
from models.auth import SignupRequest, LoginRequest, UserDetailsRequest

router = APIRouter()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")


@router.post("/auth/signup")
def signup_user(
    user: SignupRequest
):
    """
    Composite layer Auth endpoint.
    request forwarded to Auth Microservice.
    """

    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")

    body = {
        "email": user.email,
        "password": user.password,
        "uni": user.uni,
        "role": user.role,
    }
    try:
        # Call Search Microservice
        res = requests.post(
            f"{AUTH_SERVICE_URL}/auth/signup",
            json=body,
            timeout=5
        )

        if res.status_code != 200:
            
            # 2. Extract the response text (which should be the Auth Service's JSON error)
            error_text = res.text 
            
            # 3. Attempt to parse the error text back into a Python dictionary
            try:
                error_detail = res.json()
            except json.JSONDecodeError:
                # If the response isn't valid JSON, use the raw text
                error_detail = {"detail": error_text}
            
            # 4. Re-raise the error with the original status code and detail.
            # This stops the processing in the calling service and sends the clean error back to the frontend.
            raise HTTPException(
                status_code=res.status_code,
                detail=error_detail.get("detail", "Unknown error during user signup.")
            )
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Auth microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Auth microservice unavailable")


@router.post("/auth/login")
def login_user(user: LoginRequest):
    """
    Composite layer Auth endpoint.
    request forwarded to Auth Microservice.
    """

    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")

    body = {
        "email": user.email,
        "password": user.password
    }
    try:
        # Call Search Microservice
        res = requests.post(
            f"{AUTH_SERVICE_URL}/auth/login",
            json=body,
            timeout=5
        )
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail="Login Failed")
        print(res.json())
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Auth microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Auth microservice unavailable")


@router.get("/auth/get-user")
def login_user(user: UserDetailsRequest):
    """
    Composite layer Auth endpoint.
    request forwarded to Auth Microservice.
    """

    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")

    body = {
        uni: user.uni
    }
    try:
        # Call Search Microservice
        res = requests.post(
            f"{AUTH_SERVICE_URL}/auth/get-user",
            json=body,
            timeout=5
        )

        
        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Auth microservice timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Auth microservice unavailable")
