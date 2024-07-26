from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from config import settings
from logger import app_logger as logger
from user.models import User
from user.service import verify_verification_token
from user.schemas import UserRead, UserCreate
from auth.base_config import current_user
from auth.manager import send_verification
from auth.base_config import fastapi_users, auth_backend


router = APIRouter()


# Add authentication router to the router. This includes routes for login, logout.
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)


# Add register router to the router. This includes route for registration.
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)


@router.get('/ask_verification')
async def ask_verification(user: User = Depends(current_user)) -> dict:
    """
    Ask for verification for the given user.

    Args:
        user (User, optional): The user to ask for verification. Defaults to the current user.

    Returns:
        dict: A dictionary containing the status of the verification request.
            - 'status' (str): The status of the verification request. Always set to 'success'.
    """
    logger.debug(f"Asking for verification for user {user.id}")
    await send_verification(user=user)
    return {
        'status': 'success',
    }


@router.get("/verify-account", response_model=UserRead)
async def verify_user(token: str, user: User = Depends(current_user)) -> RedirectResponse:
    """
    Verify the user by checking the provided verification token.

    Args:
        token (str): The verification token to verify the user.
        user (User, optional): The user object representing the current user. Defaults to the current user.

    Raises:
        HTTPException: If the user is already verified with the provided token.

    Returns:
        RedirectResponse: A redirect response to the specified verification redirect URL.

    """
    logger.debug(f"Verifying user with verification token {token}")
    if user.is_verified:
        logger.warning(f"User with verification token {token} already verified")
        raise HTTPException(status_code=400, detail=f"User with this verification token {token} already verified")
    else:
        await verify_verification_token(token)
    return RedirectResponse(url=settings.auth.VERIFY_REDIRECT, status_code=HTTP_302_FOUND)
