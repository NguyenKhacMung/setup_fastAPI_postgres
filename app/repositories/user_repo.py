from sqlmodel import Session, select
from app.models.user import User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.exec(select(User).where(User.email == email)).first()
