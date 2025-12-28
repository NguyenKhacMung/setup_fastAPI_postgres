from uuid import UUID
from sqlmodel import Session, select
from app.models.permission import Permission
from app.repositories.base_repo import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, db: Session):
        super().__init__(db, Permission)

    def get_by_ids(self, ids: list[UUID]) -> list[Permission]:
        return self.db.exec(select(Permission).where(Permission.id.in_(ids))).all()

    def create(self, code: str):
        db_obj = Permission(code=code)
        return self.add(db_obj)

    def update(self, permission_id: UUID, code: str):
        db_obj = self.get(permission_id)
        if not db_obj:
            return None

        db_obj.code = code
        return self.add(db_obj)
