from uuid import UUID
from sqlmodel import Session, col, select
from app.models.permission import Permission
from app.repositories.base_repo import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, db: Session):
        super().__init__(db, Permission)

    def get_by_ids(self, ids: list[UUID]) -> list[Permission]:
        return list(
            self.db.exec(select(Permission).where(col(Permission.id).in_(ids))).all()
        )
