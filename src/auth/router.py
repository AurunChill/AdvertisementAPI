from fastapi import APIRouter

from .base_config import fastapi_users, auth_backend
from user.schemas import UserRead, UserCreate


router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)