import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repo import UserRepo
from app.core.database import SessionDep
from app.core.deps import require_permission, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def list_users(db: SessionDep, _: str = Depends(get_current_user)):
    return UserRepo(db).list()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    db: SessionDep,
    user_id: uuid.UUID,
    _: str = Depends(require_permission("user.read")),
):
    user = UserRepo(db).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    db: SessionDep,
    user_in: UserCreate,
    _: str = Depends(require_permission("user.create")),
):
    user = UserRepo(db).get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    return UserRepo(db).create(user_in)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    db: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
    _: str = Depends(require_permission("user.update")),
):
    user = UserRepo(db).update(user_id, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: uuid.UUID,
    db: SessionDep,
    _: str = Depends(require_permission("user.delete")),
):
    UserRepo(db).delete(user_id)
    return {"detail": "User deleted"}
