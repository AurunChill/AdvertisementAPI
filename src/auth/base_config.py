from fastapi import Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from auth.manager import get_user_manager
from user.models import User
from config import settings


# Retrieve authentication settings from the application configuration
auth_settings = settings.auth
SECRET = auth_settings.SECRET_JWT

# Configure cookie transport for JWT authentication
cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=604800)


def get_jwt_strategy() -> JWTStrategy:
    """
    Returns a JWTStrategy instance configured with the application's secret and token lifetime.

    Returns:
        JWTStrategy: The JWT strategy for handling authentication tokens.
    """
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)  # JWT will expire in 1 hour


# Create an AuthenticationBackend instance for JWT
auth_backend = AuthenticationBackend(
    name="jwt",  
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,  
)


# Initialize FastAPIUsers with the User model and the authentication backend
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


# Get the current user from the FastAPIUsers instance
current_user = fastapi_users.current_user()


async def verify_user(user: User = Depends(current_user)):
    """
    Verifies if the current user is verified.

    Args:
        user (User, optional): The current user instance, retrieved via dependency injection.

    Raises:
        HTTPException: If the user is not verified, a 403 Forbidden error is raised.

    Returns:
        User: The verified user instance.
    """
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not verified",
        )
    return user  
