from fastapi import APIRouter, HTTPException, status, Depends
from app.core.database import SessionDep
from app.core.security import verify_password, create_access_token
from app.repositories.user_repo import UserRepo
from app.schemas.auth import LoginBody, Token
from app.schemas.user import UserResponse, UserCreate
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    # body: LoginBody,
    db: SessionDep,
    body: OAuth2PasswordRequestForm = Depends(),
):
    user = UserRepo(db).get_by_username(body.username)

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    db: SessionDep,
):
    return UserRepo(db).create(user)
