"""init_roles_permissions

Revision ID: 32fb40815155
Revises: 075cc50992de
Create Date: 2025-12-27 16:44:36.693982

"""

from typing import Sequence, Union
from uuid import uuid4

# Import Enums
from app.core.constants import RoleEnum, PermissionEnum

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32fb40815155"
down_revision: Union[str, Sequence[str], None] = "075cc50992de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add Permissions from PermissionEnum
    permission_values = [p.value for p in PermissionEnum]

    for code in permission_values:
        permission_id = uuid4()
        op.execute(
            sa.text(
                "INSERT INTO permissions (id, code) VALUES (:id, :code)"
            ).bindparams(id=permission_id, code=code)
        )

    # 2. Add Roles from RoleEnum
    role_values = [r.value for r in RoleEnum]

    for name in role_values:
        role_id = uuid4()
        op.execute(
            sa.text("INSERT INTO roles (id, name) VALUES (:id, :name)").bindparams(
                id=role_id, name=name
            )
        )

    # 3. Assign all permissions to Admin role
    op.execute(
        """
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id 
        FROM roles r, permissions p 
        WHERE r.name = 'Admin'
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove all data from the tables
    op.execute("DELETE FROM role_permissions")
    op.execute("DELETE FROM roles")
    op.execute("DELETE FROM permissions")
