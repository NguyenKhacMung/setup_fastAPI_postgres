import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repo import UserRepo
from app.models.user import User
from app.core.database import SessionDep
from app.core.deps import require_permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def list_users(db: SessionDep):
    return UserRepo(db).list()


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: uuid.UUID,
    db: SessionDep,
    _: str = Depends(require_permission("user.read")),
):
    user = UserRepo(db).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: SessionDep,
    _: str = Depends(require_permission("user.create")),
):
    return UserRepo(db).create(user_in)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    db: SessionDep,
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
