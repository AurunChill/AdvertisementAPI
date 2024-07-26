from uuid import UUID
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin

from config import settings
from db import get_user_db
from logger import app_logger as logger
from user.models import User


auth_settings = settings.auth
SECRET = auth_settings.SECRET_MANAGER


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.debug(f"User {user.id} has registered.")

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ): 
        logger.debug(f"User {user.id} logged in.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
