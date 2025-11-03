from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Video(BaseModel):
    video_id: int
    offering_id: int
    prof_uni: str
    title: str
    gcs_path: str
    uploaded_at: datetime
    signed_url: Optional[str] = None
