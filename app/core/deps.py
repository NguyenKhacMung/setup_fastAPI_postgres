from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import decode_token
from app.core.database import SessionDep
from app.repositories.user_repo import UserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    db: SessionDep,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = UserRepo(db).get(user_id)
        if not user:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception


def require_permission(code: str):
    def checker(user=Depends(get_current_user)):
        if not user.role or not user.role.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No permission"
            )

        permissions = [p.code for p in user.role.permissions]
        if code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        return user

    return checker
