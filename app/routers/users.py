import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.background import P

from app.core.constants import PermissionEnum, RoleEnum
from app.schemas.user import (
    UpdateUserRoleRequest,
    UserCreateRequest,
    UserPaginationResponse,
    UserResponse,
    UserSearchRequest,
    UserUpdateRequest,
)
from app.repositories.user_repo import UserRepository
from app.core.database import SessionDep
from app.core.deps import require_permissions, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(db: SessionDep, _: str = Depends(get_current_user)):
    return UserRepository(db).get_all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    db: SessionDep,
    user_id: uuid.UUID,
    _: str = Depends(require_permissions([PermissionEnum.READ])),
):
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    db: SessionDep,
    body: UserCreateRequest,
    _: str = Depends(require_permissions([PermissionEnum.CREATE])),
):
    user = UserRepository(db).get_by_username(body.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    return UserRepository(db).create(body)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    db: SessionDep,
    user_id: uuid.UUID,
    body: UserUpdateRequest,
    _: str = Depends(require_permissions([PermissionEnum.UPDATE])),
):
    user = UserRepository(db).update(user_id, body)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: uuid.UUID,
    body: UpdateUserRoleRequest,
    db: SessionDep,
    _: str = Depends(require_permissions([PermissionEnum.UPDATE])),
):
    user = UserRepository(db).update_role(user_id, body.role_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User or Role not found"
        )
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: uuid.UUID,
    db: SessionDep,
    _: str = Depends(require_permissions([PermissionEnum.DELETE])),
):
    user = UserRepository(db).delete(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"detail": "User deleted"}


@router.post("/search", response_model=UserPaginationResponse)
def search_users(
    db: SessionDep,
    body: UserSearchRequest,
    _: str = Depends(require_permissions([PermissionEnum.READ])),
):
    return UserRepository(db).search(body)
