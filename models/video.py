from pydantic import BaseModel
from typing import Optional


class Video(BaseModel):
    video_id: str
    title: str
    gcs_path: str
    uploaded_at: str
    course_id: str
    course_name: str
    prof_uni: str

    # Optional if you want to return offering metadata
    semester: Optional[str] = None
    year: Optional[int] = None
    section: Optional[int] = None
