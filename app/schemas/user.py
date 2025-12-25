import uuid
from sqlmodel import Field
from app.models.user import UserBase


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=12)


class UserResponse(UserBase):
    id: uuid.UUID
    role_id: uuid.UUID | None = None


class UserUpdate(UserBase):
    password: str
    role_id: uuid.UUID | None = None
