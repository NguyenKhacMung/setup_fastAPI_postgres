from sqlmodel import Session
from app.core.database import engine
from app.models.master.role import Role
from app.models.master.permission import Permission

ROLES = [
    "PLATFORM_ADMIN",
    "PLATFORM_USER",
    "TENANT_ADMIN",
    "TENANT_USER",
    "TENANT_SENIOR",
]

PERMISSIONS = [
    "USER_MANAGE",
    "MEAL_PLAN_READ",
    "MEAL_PLAN_WRITE",
    "CONVERSATION_READ",
]


def run():
    with Session(engine) as session:
        session.exec('SET search_path TO "master"')

        for r in ROLES:
            session.add(Role(role_name=r))

        for p in PERMISSIONS:
            session.add(Permission(permission_name=p))

        session.commit()


if __name__ == "__main__":
    run()
