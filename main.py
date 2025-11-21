# main.py  — Composite Microservice (delegator/orchestrator)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

print(f"[DEBUG] Loaded AUTH_SERVICE_URL = {os.getenv('AUTH_SERVICE_URL')}")
print(f"[DEBUG] Loaded SEARCH_SERVICE_URL = {os.getenv('SEARCH_SERVICE_URL')}")
print(f"[DEBUG] Loaded SEARCH_SERVICE_URL = {os.getenv('UPLOAD_SERVICE_URL')}")

app = FastAPI(title="Composite Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from resources.video_resource import router as video_router
from resources.auth_resource import router as auth_router
app.include_router(video_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Composite Service is running"}

@app.get("/healthz")
def health():
    return {"ok": True}
