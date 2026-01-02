from fastapi import Depends, HTTPException

from app.api.deps import get_current_user


def IAuthz(roles: list[str], permissions: list[str]):
    def wrapper(user=Depends(get_current_user)):
        if user.system_role not in roles:
            raise HTTPException(403, "Role denied")
        if not set(user.permissions) & set(permissions):
            raise HTTPException(403, "Permission denied")
        return user

    return wrapper


# using in router
#  user = Depends(IAuthz(
#         roles=["TENANT_SENIOR"],
#         permissions=["MEAL_PLAN_READ", "MEAL_PLAN_WRITE"]
#     ))
