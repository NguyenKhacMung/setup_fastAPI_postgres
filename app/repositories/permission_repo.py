from uuid import UUID
from sqlmodel import Session, select
from app.models.permission import Permission


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Permission]:
        return list(self.db.exec(select(Permission)))

    def get_by_id(self, permission_id: UUID):
        return self.db.get(Permission, permission_id)

    def get_by_ids(self, ids: list[UUID]) -> list[Permission]:
        return self.db.exec(select(Permission).where(Permission.id.in_(ids))).all()

    def create(self, code: str):
        db_obj = Permission(code=code)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, permission_id: UUID, code: str):
        db_obj = self.get_by_id(permission_id)
        if db_obj:
            db_obj.code = code
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, permission_id: UUID):
        db_obj = self.get_by_id(permission_id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj
