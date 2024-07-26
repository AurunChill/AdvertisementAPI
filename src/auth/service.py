
import secrets

from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from config import settings
from db import async_session_maker
from mail.utils import send_email_verification_msg
from user.models import User
from user.service import update_user_verification_token
from user.tasks import delete_user_verification_token_task


password_hash = PasswordHash((Argon2Hasher(),))
password_helper = PasswordHelper(password_hash)


async def verify_password(stored_hashed_password: str, given_password: str) -> bool:
    """
    Verify if the given password matches the stored hashed password.
    
    Args:
        stored_hashed_password (str): The hashed password stored in the database.
        given_password (str): The password provided by the user.
    
    Returns:
        bool: True if the password is verified and the hashed password is updated, False otherwise.
    """
    is_verified, updated_hash = password_helper.verify_and_update(given_password, stored_hashed_password)
    if is_verified and updated_hash:
        async with async_session_maker() as session:
            await session.execute(
                f"UPDATE {User.__tablename__} SET hashed_password = :new_hash WHERE hashed_password = :old_hash",
                {"new_hash": updated_hash, "old_hash": stored_hashed_password}
            )
            await session.commit()
    return is_verified


async def send_verification(user: User) -> str:
    """
    Sends a verification email to the given user.

    Args:
        user (User): The user to send the verification email to.

    Returns:
        str: The verification token generated for the user.
    """
    token = secrets.token_hex(16)
    await update_user_verification_token(user_id=user.id, token=token)
    await send_email_verification_msg(user=user, verification_token=token)
    delete_user_verification_token_task.apply_async(
        (user.id,), countdown=settings.auth.VERIFY_TOKEN_EXPIRATION
    )
    return token