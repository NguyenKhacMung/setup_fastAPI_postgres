import uuid
from typing import List, Optional
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[User]:
        return list(self.db.exec(select(User)))

    def get(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.exec(select(User).where(User.username == username)).first()

    def create(self, user_in: UserCreate) -> User:
        user = User(
            username=user_in.username, password_hash=hash_password(user_in.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: uuid.UUID, user_in: UserUpdate) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        if user_in.username is not None:
            user.username = user_in.username
        if user_in.password is not None:
            user.password_hash = hash_password(user_in.password)
        if user_in.role_id is not None:
            user.role_id = user_in.role_id
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: uuid.UUID) -> None:
        user = self.get(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
