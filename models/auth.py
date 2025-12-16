from pydantic import BaseModel, EmailStr
from typing import Literal
class SignupRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str
    uni: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    password: str

class UserDetailsRequest(BaseModel):
    uni: str

class UpdateRoleRequest(BaseModel):
    email: EmailStr        # ensures valid email format
    role: Literal["student", "faculty"]