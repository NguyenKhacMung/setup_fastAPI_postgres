import uuid
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    role_id: uuid.UUID | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    role_id: uuid.UUID | None = None
