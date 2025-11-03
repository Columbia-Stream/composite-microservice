from fastapi import Header, HTTPException
import requests
import os
from dotenv import load_dotenv

def verify_token(authorization: str = Header(None)):
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
    AUTH_URL = os.getenv("AUTH_SERVICE_URL")

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not AUTH_URL:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL not set")

    print(f"[DEBUG] Verifying token via: {AUTH_URL}")
    print(f"[DEBUG] Header being sent: {authorization[:50]}...")  # truncate for safety

    try:
        res = requests.get(AUTH_URL, headers={"Authorization": authorization}, timeout=5)
        print(f"[DEBUG] Auth responded with status: {res.status_code}")
        print(f"[DEBUG] Auth response body: {res.text}")

        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Auth verification failed: {res.text}"
            )

        data = res.json()
        return {
            "uid": data.get("uid"),
            "email": data.get("email"),
            "role": data.get("role", "faculty"),
        }

    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Auth service timeout")
    except requests.ConnectionError:
        raise HTTPException(status_code=503, detail="Auth service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth verification error: {str(e)}")
