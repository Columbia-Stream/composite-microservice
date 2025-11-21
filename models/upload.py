from pydantic import BaseModel
class VideoUpload(BaseModel):
    offering_id: int
    prof_uni: str
    videoTitle: str