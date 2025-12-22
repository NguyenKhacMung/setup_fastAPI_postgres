from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.repositories.user_repo import UserRepo

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = UserRepo(db).get_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": user.id})
    return {"access_token": token}
