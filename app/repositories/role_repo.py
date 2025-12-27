from uuid import UUID
from sqlmodel import Session, select
from app.models.role import Role
from app.repositories.permission_repo import PermissionRepository
from app.schemas.role import RoleUpdateRequest


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
        self.permission_repo = PermissionRepository(db)

    def get_all(self):
        return self.db.exec(select(Role)).all()

    def get_by_id(self, role_id: UUID):
        return self.db.get(Role, role_id)

    def get_by_name(self, name: str) -> Role | None:
        return self.db.exec(select(Role).where(Role.name == name)).first()

    def create(self, name: str, permission_ids: list[UUID]):
        role = Role(name=name)

        if permission_ids:
            perms = self.permission_repo.get_by_ids(permission_ids)
            role.permissions = perms

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update(self, role_id: UUID, role: RoleUpdateRequest):
        db_role = self.get_by_id(role_id)
        if not db_role:
            return None

        if role.name:
            db_role.name = role.name

        if role.permission_ids is not None:
            perms = self.permission_repo.get_by_ids(role.permission_ids)
            db_role.permissions = perms

        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def delete(self, role_id: UUID):
        db_role = self.get_by_id(role_id)
        if db_role:
            self.db.delete(db_role)
            self.db.commit()
            return True
        return False
