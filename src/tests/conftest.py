import asyncio

from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from config import settings
from main import app
from user.service import get_user_by_username


# Define the base API prefix for versioning
api_prefix = "/api/v1"

# Dictionary mapping routes for authentication and advertisement URLs
test_urls = {
    "auth": {
        "register": "/auth/register",
        "login": "/auth/login",
        "logout": "/auth/logout",
        "ask_verification": "/auth/ask_verification",
        "verify_account": "/auth/verify-account",
    },
    "advertisement": {
        "get_all_advertisements": f"{api_prefix}/advertisement/",
        "create_advertisement": f"{api_prefix}/advertisement/",
        "update_advertisement": f"{api_prefix}/advertisement/",
        "get_advertisement": f"{api_prefix}/advertisement/",
        "delete_advertisement": f"{api_prefix}/advertisement/",
    },
}


# Fixture to create an asynchronous event loop for the test session
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Fixture providing mock user data for testing
@pytest_asyncio.fixture
async def user_data() -> dict:
    return {
        "username": "test_user",
        "email": "test@ex.com",
        "password": "SuperUsername1233",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }


# Fixture providing mock advertisement data for testing
@pytest_asyncio.fixture
async def advertisement_data() -> dict:
    return {
        "title": "string",
        "author": "string",
        "views_count": 0,
        "position": 1,
    }


# Fixture to create an async client for making HTTP requests in tests
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=settings.test.BASE_URL
    ) as client:
        yield client


# Fixture to create an authenticated async client after registering and logging in a user
@pytest_asyncio.fixture
async def auth_async_client(async_client: AsyncClient, user_data: dict) -> AsyncClient:
    # Register the user and get response data
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"),
        json={
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    # Log in to obtain authentication cookies
    login_response = await async_client.post(
        url=test_urls["auth"].get("login"),
        data={
            "username": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    # Set the authentication cookies in the async client
    async_client.cookies = {
        "bonds": login_response.headers.get("set-cookie").split(";")[0][6:],
        "user_id": response_data.json().get("id"),
    }
    return async_client


@pytest_asyncio.fixture
async def auth_async_verified_client(
    auth_async_client: AsyncClient, user_data: dict
) -> AsyncClient:
        # Verify the account
    await auth_async_client.get(
        url=test_urls["auth"].get("ask_verification")
    )
    user = await get_user_by_username(username=user_data.get("username"))
    await auth_async_client.get(
        url=test_urls["auth"].get("verify_account"),
        params={"token": user.verification_token},
    )
    return auth_async_client
