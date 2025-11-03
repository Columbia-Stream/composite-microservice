from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from utils.auth import verify_token
from services.video_service import search_videos
from dotenv import load_dotenv
import os

# --- Load environment variables ---
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# --- Sanity check for debugging ---
print(f"[DEBUG] Loaded AUTH_SERVICE_URL = {os.getenv('AUTH_SERVICE_URL')}")
print(f"[DEBUG] Loaded DB_HOST = {os.getenv('DB_HOST')}")

# --- Initialize FastAPI app ---
app = FastAPI(title="DBService", version="0.3.0")

# --- CORS setup (allow frontend & other microservices to talk to it) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for local dev, later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Root health route ---
@app.get("/")
def root():
    return {"message": "DBService is running"}

@app.get("/healthz")
def health():
    return {"ok": True}

# --- Main video search endpoint ---
@app.get("/videos/search")
def search_videos_route(
    q: str = Query(None),
    offering_id: int = Query(None),
    prof: str = Query(None),
    limit: int = Query(20),
    user=Depends(verify_token)   # 🔒 ensures every request verifies via Auth service
):
    """
    Endpoint that verifies the user's Firebase token via the Auth microservice,
    then queries the MySQL database for matching videos.
    """
    print(f"[DEBUG] Authenticated user: {user}")
    return search_videos(q, offering_id, prof, limit)
