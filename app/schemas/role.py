from uuid import UUID
from app.core.constants import RoleEnum
from app.models import RoleBase
from app.schemas.permission import PermissionResponse


class RoleCreateRequest(RoleBase):
    name: RoleEnum
    permission_ids: list[UUID] | None = None


class RoleUpdateRequest(RoleBase):
    name: RoleEnum | None = None
    permission_ids: list[UUID] | None = None


class RoleResponse(RoleBase):
    id: UUID
    permissions: list[PermissionResponse] = []
