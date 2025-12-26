import uuid
from app.models.permission import PermissionBase


class PermissionCreate(PermissionBase): ...


class PermissionResponse(PermissionBase):
    id: uuid.UUID
