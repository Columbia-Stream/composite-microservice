from pydantic import BaseModel, EmailStr
class SignupRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
    uni: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
