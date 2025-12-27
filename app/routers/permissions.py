from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.core.database import SessionDep
from app.core.deps import require_permissions
from app.repositories.permission_repo import PermissionRepository
from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)
from app.core.constants import PermissionEnum

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.get("/", response_model=list[PermissionResponse])
def list_permissions(
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.READ])),
):
    return PermissionRepository(db).get_all()


@router.post(
    "/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED
)
def create_permission(
    body: PermissionCreate,
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.CREATE])),
):
    return PermissionRepository(db).create(body.code)


@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: UUID,
    body: PermissionUpdate,
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.UPDATE])),
):
    updated = PermissionRepository(db).update(permission_id, body.code)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return updated


@router.delete("/{permission_id}")
def delete_permission(
    permission_id: UUID,
    db: SessionDep,
    _=Depends(require_permissions([PermissionEnum.DELETE])),
):
    if not PermissionRepository(db).delete(permission_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return {"message": "Deleted successfully"}
