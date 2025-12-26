import uuid
from typing import List
from app.models import RoleBase
from app.schemas.permission import PermissionResponse


class RoleCreate(RoleBase): ...


class RoleResponse(RoleBase):
    id: uuid.UUID
    permissions: List[PermissionResponse] = []


class RoleUpdateRequest(RoleBase):
    permissions: List[PermissionResponse] = []
