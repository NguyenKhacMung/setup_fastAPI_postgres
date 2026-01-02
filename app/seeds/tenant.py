from sqlmodel import Session
from app.core.database import engine
from app.models.tenant.role import TenantRole
from app.models.tenant.permission import TenantPermission

TENANT_ROLES = [
    "TENANT_ADMIN",
    "TENANT_USER",
    "TENANT_SENIOR",
]

TENANT_PERMISSIONS = [
    "MEAL_PLAN_READ",
    "MEAL_PLAN_WRITE",
    "CONVERSATION_READ",
]


def run(schema: str):
    with Session(engine) as session:
        session.exec(f'SET search_path TO "{schema}"')

        for r in TENANT_ROLES:
            session.add(TenantRole(role_name=r))

        for p in TENANT_PERMISSIONS:
            session.add(TenantPermission(permission_name=p))

        session.commit()
