import pytest
from httpx import AsyncClient

from conftest import test_urls
from advertisement.service import delete_advertisement


@pytest.mark.asyncio
async def test_create_advertisement_successfully(
    auth_async_verified_client: AsyncClient, advertisement_data: dict
):
    response = await auth_async_verified_client.post(
        test_urls["advertisement"].get("create_advertisement"), json=advertisement_data
    )
    created_data = response.json()
    assert (
        response.status_code == 201 and created_data.get("title") == "string"
    )  # замените "title" на ключ вашего объявления
    await delete_advertisement(created_data.get("id"))


@pytest.mark.asyncio
async def test_create_advertisement_unauthorized(
    async_client: AsyncClient, advertisement_data: dict
):
    response = await async_client.post(
        test_urls["advertisement"].get("create_advertisement"), json=advertisement_data
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_advertisement_incorrect(auth_async_verified_client: AsyncClient):
    response = await auth_async_verified_client.post(
        test_urls["advertisement"].get("create_advertisement"), json={}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_advertisements(
    auth_async_verified_client: AsyncClient, advertisement_data: dict
):
    created_ids = []
    for _ in range(5):
        create_response = await auth_async_verified_client.post(
            test_urls["advertisement"].get("create_advertisement"),
            json=advertisement_data,
        )
        created_ids.append(create_response.json().get("id"))
    response = await auth_async_verified_client.get(
        test_urls["advertisement"].get("get_all_advertisements")
    )
    assert response.status_code == 200
    for id in created_ids:
        await delete_advertisement(id)


@pytest.mark.asyncio
async def test_get_all_advertisements_empty(auth_async_verified_client: AsyncClient):
    response = await auth_async_verified_client.get(
        test_urls["advertisement"].get("get_all_advertisements")
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_advertisement_successfully(
    auth_async_verified_client: AsyncClient, advertisement_data: dict
):
    create_response = await auth_async_verified_client.post(
        test_urls["advertisement"].get("create_advertisement"), json=advertisement_data
    )
    advertisement_data = create_response.json()
    new_data = advertisement_data.copy()
    new_data["title"] = "new string"  # замените "title" на ключ вашего объявления
    response = await auth_async_verified_client.put(
        test_urls["advertisement"].get("update_advertisement"), json=new_data
    )
    updated_data = response.json()
    assert (
        response.status_code == 200
        and updated_data.get("title") == "new string"
        and updated_data.get("city") == advertisement_data.get("city")
    )
    await delete_advertisement(advertisement_data.get("id"))


@pytest.mark.asyncio
async def test_update_advertisement_unauthorized(
    async_client: AsyncClient, advertisement_data: dict
):
    response = await async_client.put(
        test_urls["advertisement"].get("update_advertisement"), json=advertisement_data
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_advertisement_incorrect(auth_async_verified_client: AsyncClient):
    response = await auth_async_verified_client.put(
        test_urls["advertisement"].get("update_advertisement"), json={}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user_advertisement(
    auth_async_verified_client: AsyncClient, advertisement_data: dict
):
    create_response = await auth_async_verified_client.post(
        test_urls["advertisement"].get("create_advertisement"), json=advertisement_data
    )
    created_data = create_response.json()
    response = await auth_async_verified_client.get(
        test_urls["advertisement"].get("get_advertisement")
        + f"{created_data.get('id')}"
    )
    assert response.status_code == 200 and response.json().get(
        "id"
    ) == created_data.get("id")
    await delete_advertisement(created_data.get("id"))


@pytest.mark.asyncio
async def test_get_user_advertisement_unauthorized(async_client: AsyncClient):
    response = await async_client.get(
        test_urls["advertisement"].get("get_advertisement") + "1"
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_advertisement_successfully(
    auth_async_verified_client: AsyncClient, advertisement_data: dict
):
    create_response = await auth_async_verified_client.post(
        test_urls["advertisement"].get("create_advertisement"), json=advertisement_data
    )
    created_data = create_response.json()
    response = await auth_async_verified_client.delete(
        test_urls["advertisement"].get("delete_advertisement")
        + f"{created_data.get('id')}"
    )
    assert response.status_code in [200, 204]
