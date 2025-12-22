import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.repositories.user_repo import UserRepo
from app.core.database import get_db
from app.core.deps import require_permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def list_users(
    _: str = Depends(require_permission("user.read")), db: Session = Depends(get_db)
):
    return UserRepo(db).list()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: uuid.UUID,
    _: str = Depends(require_permission("user.read")),
    db: Session = Depends(get_db),
):
    user = UserRepo(db).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    _: str = Depends(require_permission("user.create")),
    db: Session = Depends(get_db),
):
    return UserRepo(db).create(user_in)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    _: str = Depends(require_permission("user.update")),
    db: Session = Depends(get_db),
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
    _: str = Depends(require_permission("user.delete")),
    db: Session = Depends(get_db),
):
    UserRepo(db).delete(user_id)
    return {"detail": "User deleted"}
