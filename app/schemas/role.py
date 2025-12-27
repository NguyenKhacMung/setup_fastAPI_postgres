from uuid import UUID
from app.core.constants import RoleEnum
from app.models import RoleBase
from app.schemas.permission import PermissionResponse


class RoleCreate(RoleBase): ...


class RoleResponse(RoleBase):
    id: UUID
    permissions: list[PermissionResponse] = []


class RoleUpdateRequest(RoleBase):
    name: RoleEnum | None = None
    permission_ids: list[UUID] | None = None


class RoleCreateRequest(RoleBase):
    name: str
    permission_ids: list[UUID] = []
