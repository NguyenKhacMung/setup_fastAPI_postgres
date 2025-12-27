from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.constants import PermissionEnum
from app.core.database import SessionDep
from app.core.deps import require_permissions
from app.repositories.role_repo import RoleRepository
from app.schemas.role import RoleCreateRequest, RoleResponse, RoleUpdateRequest


router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleResponse])
def get_roles(db: SessionDep, _=Depends(require_permissions([PermissionEnum.READ]))):
    return RoleRepository(db).get_all()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    body: RoleCreateRequest,
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.CREATE])),
):
    return RoleRepository(db).create(body.name, body.permission_ids)


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: UUID,
    body: RoleUpdateRequest,
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.UPDATE])),
):
    role = RoleRepository(db).update(role_id, body)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    return role


@router.delete("/{role_id}")
def delete_role(
    role_id: UUID,
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.DELETE])),
):
    if not RoleRepository(db).delete(role_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    return {"message": "Deleted successfully"}
