from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Video(BaseModel):
    video_id: int
    offering_id: int
    course_id: str
    course_name: str
    prof_uni: str
    title: str
    gcs_path: Optional[str] = None
    uploaded_at: Optional[datetime] = None

    # Optional if you want to return offering metadata
    semester: Optional[str] = None
    year: Optional[int] = None
    section: Optional[int] = None