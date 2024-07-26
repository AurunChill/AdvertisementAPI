import asyncio

from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from config import settings
from main import app

api_prefix = "/api/v1"

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


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


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


@pytest.fixture
async def advertisement_data() -> dict:
    return   {
        "title": "string",
        "author": "string",
        "views_count": 0,
        "position": 1,
  }


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=settings.test.BASE_URL
    ) as client:
        yield client


@pytest_asyncio.fixture
async def auth_async_client(async_client: AsyncClient, user_data: dict) -> AsyncClient:
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"),
        json={
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    login_response = await async_client.post(
        url=test_urls["auth"].get("login"),
        data={
            "username": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    async_client.cookies = {
        "bonds": login_response.headers.get("set-cookie").split(";")[0][6:],
        "user_id": response_data.json().get("id"),
    }
    return async_client
