from fastapi import APIRouter, Depends
from app.core.deps import require_permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def list_users(user=Depends(require_permission("user.read"))):
    return ["user1", "user2"]
