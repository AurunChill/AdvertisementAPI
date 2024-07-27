from uuid import UUID
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin

from config import settings
from db import get_user_db
from logger import app_logger as logger
from auth.service import send_verification
from user.models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = verification_token_secret = settings.auth.SECRET_MANAGER

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Asynchronously handles the event after a user has been registered.

        Args:
            user (User): The user who has been registered.
            request (Optional[Request], optional): The request object. Defaults to None.

        Returns:
            None
        """
        logger.debug(f"User {user.id} has registered.")

    async def (
            self, user: User, 
            request: Optional[Request] = None, 
            response: Optional[Response] = None
        ): 
        """
        Asynchronously handles the event after a user has been logged in.

        Args:
            user (User): The user who has been logged in.
            request (Optional[Request], optional): The request object. Defaults to None.
            response (Optional[Response], optional): The response object. Defaults to None.

        Returns:
            None
        """
        logger.debug(f"User {user.id} logged in.")
        if not user.is_verified:
            await send_verification(user)

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        """
        Asynchronously handles the event after a request for user verification has been made.

        Args:
            user (User): The user for whom the verification request has been made.
            token (str): The verification token generated for the user.
            request (Optional[Request], optional): The request object. Defaults to None.

        Returns:
            None
        """
        token = await send_verification(user=user)
        logger.debug(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Asynchronously retrieves a user manager instance for the given user database.
    Args:
        user_db (Depends, optional): A dependency that provides a user database. Defaults to Depends(get_user_db).

    Yields:
        UserManager: A user manager instance for the given user database.
    """
    yield UserManager(user_db)