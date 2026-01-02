from fastapi import Depends, HTTPException

from app.api.deps import get_current_user


def IAuthz(roles: list[str], permissions: list[str]):
    def decorator(fn):
        def wrapper(*args, user=Depends(get_current_user), **kwargs):
            if user.system_role not in roles:
                raise HTTPException(403)
            if not set(user.permissions) & set(permissions):
                raise HTTPException(403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
