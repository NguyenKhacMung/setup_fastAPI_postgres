import uuid
from pydantic import BaseModel


class PermissionBase(BaseModel):
    code: str


class PermissionCreate(PermissionBase): ...


class PermissionRead(PermissionBase):
    id: uuid.UUID
