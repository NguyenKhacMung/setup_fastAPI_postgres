import re
from uuid import UUID
from sqlmodel import Session, select
from app.models.role import Role
from app.repositories.base_repo import BaseRepository
from app.repositories.permission_repo import PermissionRepository
from app.schemas.role import RoleUpdateRequest


class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: Session):
        super().__init__(db, Role)
        self.permission_repo = PermissionRepository(db)

    def get_by_name(self, name: str) -> Role | None:
        return self.db.exec(select(Role).where(Role.name == name)).first()

    def create(self, name: str, permission_ids: list[UUID]) -> Role:
        role = Role(name=name)

        if permission_ids:
            perms = self.permission_repo.get_by_ids(permission_ids)
            role.permissions = perms

        return self.add(role)

    def update(self, role_id: UUID, role: RoleUpdateRequest) -> Role | None:
        db_role = self.get(role_id)
        if not db_role:
            return None

        if role.name:
            db_role.name = role.name

        if role.permission_ids:
            perms = self.permission_repo.get_by_ids(role.permission_ids)
            db_role.permissions = perms

        return self.add(db_role)
