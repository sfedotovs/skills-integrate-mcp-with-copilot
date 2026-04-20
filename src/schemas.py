"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    name: str
    description: str
    schedule: str
    max_participants: int = 20


class ActivityCreate(ActivityBase):
    advisor_id: Optional[int] = None


class ActivityResponse(ActivityBase):
    id: int
    advisor_id: Optional[int]
    created_at: datetime
    participants: List[UserResponse] = []

    class Config:
        from_attributes = True


class AttendanceBase(BaseModel):
    user_id: int
    activity_id: int
    attended: bool


class AttendanceResponse(AttendanceBase):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True
