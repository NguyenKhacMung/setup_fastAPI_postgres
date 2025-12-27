from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.core.constants import PermissionEnum
from app.core.security import decode_token
from app.core.database import SessionDep
from app.models.user import User
from app.repositories.user_repo import UserRepository

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
security = HTTPBearer()


def get_current_user(
    db: SessionDep,
    auth: HTTPAuthorizationCredentials = Depends(security),
    # token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = auth.credentials
        payload = decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = UserRepository(db).get(user_id)
        if not user:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception


def require_permissions(required_permissions: list[PermissionEnum]):
    def permission_checker(current_user: User = Depends(get_current_user)):
        if not current_user.role or not current_user.role.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No permission"
            )

        # Get list of permission codes from user's role
        user_permissions = {p.code for p in current_user.role.permissions}

        # Check if all required permissions are present
        for permission in required_permissions:
            if permission.value not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission: {permission.value}",
                )
        return current_user

    return permission_checker
