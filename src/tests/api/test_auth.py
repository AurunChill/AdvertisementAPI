import pytest
from httpx import AsyncClient

from conftest import test_urls
from user.service import get_user_by_username, delete_user


@pytest.mark.asyncio
async def test_register_successfully(async_client: AsyncClient, user_data: dict):
    db_user = await get_user_by_username(username=user_data.get("username"))
    if db_user:
        await delete_user(db_user)
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"), json=user_data
    )
    db_user = await get_user_by_username(username=user_data.get("username"))
    data = response_data.json()
    assert db_user.username == data.get("username")
    assert db_user.email == data.get("email")
    assert response_data.status_code == 201 and db_user is not None
    await delete_user(db_user)


@pytest.mark.asyncio
async def test_register_already(async_client: AsyncClient, user_data: dict):
    _ = await async_client.post(url=test_urls["auth"].get("register"), json=user_data)
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"), json={
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        }
    )
    db_user = await get_user_by_username(username=user_data.get("username"))
    assert response_data.status_code == 400 and db_user is not None
    await delete_user(db_user)


@pytest.mark.asyncio
async def test_register_invalid(async_client: AsyncClient):
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"), json={}
    )
    assert response_data.status_code == 422


@pytest.mark.asyncio
async def test_register_with_missing_fields(async_client: AsyncClient):
    user_data = {
        "username": "test_user",
        "email": "test@ex.com",
    }
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"), json=user_data
    )
    assert response_data.status_code == 422


@pytest.mark.asyncio
async def test_register_with_invalid_email(async_client: AsyncClient, user_data: dict):
    user_data["email"] = "invalid-email"
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"), json=user_data
    )
    assert response_data.status_code == 422


@pytest.mark.asyncio
async def test_register_with_weak_password(async_client: AsyncClient, user_data: dict):
    user_data["password"] = "123"
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"), json=user_data
    )
    assert response_data.status_code == 422


@pytest.mark.asyncio
async def test_login_successfully(async_client: AsyncClient, user_data: dict):
    _ = await async_client.post(url=test_urls["auth"].get("register"), json=user_data)
    response = await async_client.post(
        url=test_urls["auth"].get("login"),
        data={
            "username": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    assert response.status_code in [200, 204]
    await delete_user(await get_user_by_username(username=user_data.get("username")))


@pytest.mark.asyncio
async def test_login_unsuccessfully(async_client: AsyncClient, user_data: dict):
    response = await async_client.post(
        url=test_urls["auth"].get("login"),
        data={"username": user_data.get("email"), "password": "wrongpassword"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_with_invalid_format(async_client: AsyncClient):
    response = await async_client.post(
        url=test_urls["auth"].get("login"),
        data={"username": "not-an-email", "password": "password"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_logout_successfully(auth_async_verified_client: AsyncClient, user_data: dict):
    logout_response = await auth_async_verified_client.post(url=test_urls["auth"].get("logout"))
    assert logout_response.status_code in [200, 204]
    await delete_user(await get_user_by_username(username=user_data.get("username")))


@pytest.mark.asyncio
async def test_ask_verification_successfully(auth_async_verified_client: AsyncClient):
    response = await auth_async_verified_client.get(
        url=test_urls["auth"].get("ask_verification")
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_already_verified(auth_async_verified_client: AsyncClient, user_data: dict):
    user = await get_user_by_username(username=user_data.get("username"))
    response = await auth_async_verified_client.get(
        url=test_urls["auth"].get("verify_account"),
        params={"token": user.verification_token},
    )
    user = await get_user_by_username(username=user_data.get("username"))
    assert response.status_code == 400 and user.is_verified


@pytest.mark.asyncio
async def test_verify_account_wrong_token(auth_async_verified_client: AsyncClient):
    response = await auth_async_verified_client.get(
        url=test_urls["auth"].get("verify_account"),
        params={"token": "wrong_token"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_verify_account_unsuccessfully(auth_async_verified_client: AsyncClient):
    response = await auth_async_verified_client.get(
        url=test_urls["auth"].get("verify_account"),
        params={},
    )
    assert response.status_code == 422