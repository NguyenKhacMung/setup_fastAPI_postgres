from fastapi import APIRouter

from app.api.routers import auth, login, permissions, roles, users


api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(permissions.router)
