from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserRole(str, Enum):
    RESEARCHER = "researcher"
    RESEARCH_LEAD = "research_lead"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    roles: List[UserRole] = [UserRole.RESEARCHER]
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str
    roles: List[UserRole]
    exp: datetime