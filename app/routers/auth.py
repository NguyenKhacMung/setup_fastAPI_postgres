from fastapi import APIRouter, HTTPException, status
from app.core.database import SessionDep
from app.core.security import verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, AuthResponse
from app.schemas.user import UserResponse, UserCreateRequest

# from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=AuthResponse)
def login(
    db: SessionDep,
    # body: OAuth2PasswordRequestForm = Depends(),
    body: LoginRequest,
):
    user = UserRepository(db).get_by_username(body.username)

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
    db: SessionDep,
    body: UserCreateRequest,
):
    userExists = UserRepository(db).get_by_username(body.username)
    if userExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    return UserRepository(db).create(body)
