from uuid import UUID
from app.models.permission import PermissionBase


class PermissionCreate(PermissionBase): ...


class PermissionUpdate(PermissionBase): ...


class PermissionResponse(PermissionBase):
    id: UUID
