import uuid
from typing import Any, Literal
from pydantic import BaseModel, Field
from app.core.constants import RoleEnum
from app.models import UserBase
from app.schemas.role import RoleResponse


class UserCreateRequest(UserBase):
    password: str = Field(min_length=8, max_length=12)


class UserResponse(UserBase):
    id: uuid.UUID
    role: RoleResponse | None = None


class UserUpdateRequest(UserBase):
    password: str | None = None
    role_id: uuid.UUID | None = None


class UpdateUserRoleRequest(BaseModel):
    role_name: RoleEnum


class UserSearchRequest(BaseModel):
    search: str | None = None
    filter: dict[str, str] | None = None
    sort_by: str | None = "username"
    sort_order: Literal["asc", "desc"] = "asc"
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class UserPaginationResponse(BaseModel):
    items: list[UserResponse]
    filter: dict[str, Any] | None
    sort_by: str
    sort_order: str
    total: int
    page: int
    size: int
    pages: int
