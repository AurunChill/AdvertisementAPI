from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from logger import app_logger as logger
from auth.base_config import current_user
from user.models import User
from advertisement.schemas import AdvertisementCreate, AdvertisementRead, AdvertisementUpdate
from advertisement.service import (
    get_advertisements_all, get_advertisement_by_id, 
    create_advertisement, delete_advertisement, update_advertisement
)


router = APIRouter()


@router.get("/", response_model=list[AdvertisementRead])
async def read_advertisements(user: User = Depends(current_user)) -> list[AdvertisementRead]:
    """
    Asynchronously retrieves all advertisements.

    Args:
        user (User): The current user, required for authorization.

    Returns:
        list[AdvertisementRead]: A list of all advertisements.
    """
    logger.info("Get all advertisements")
    return await get_advertisements_all()


@router.get("/{advertisement_id}", response_model=AdvertisementRead)
async def read_advertisement_by_id(advertisement_id: int, user: User = Depends(current_user)) -> AdvertisementRead:
    """
    Asynchronously retrieves an advertisement by its ID.

    Args:
        advertisement_id (int): The ID of the advertisement to retrieve.
        user (User): The current user, required for authorization.

    Raises:
        HTTPException: If the advertisement with the given ID is not found.

    Returns:
        AdvertisementRead: The advertisement corresponding to the given ID.
    """
    logger.info(f"Get advertisement with id {advertisement_id}")
    advertisement = await get_advertisement_by_id(advertisement_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AdvertisementRead)
async def create_advertisement_endpoint(new_advertisement: AdvertisementCreate, user: User = Depends(current_user)) -> AdvertisementRead:
    """
    Asynchronously creates a new advertisement.

    Args:
        new_advertisement (AdvertisementCreate): The new advertisement data.
        user (User): The current user, required for authorization.

    Returns:
        AdvertisementRead: The created advertisement.
    """
    logger.info("Create new advertisement")
    return await create_advertisement(new_advertisement)


@router.delete("/{advertisement_id}")
async def delete_advertisement_endpoint(advertisement_id: int, user: User = Depends(current_user)) -> dict:
    """
    Asynchronously deletes an advertisement by its ID.

    Args:
        advertisement_id (int): The ID of the advertisement to delete.
        user (User): The current user, required for authorization.

    Raises:
        HTTPException: If the advertisement with the given ID is not found.

    Returns:
        dict: A confirmation message indicating the advertisement has been deleted.
    """
    logger.info(f"Delete advertisement with id {advertisement_id}")  
    result = await delete_advertisement(advertisement_id)
    if not result:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return {"detail": "Advertisement deleted"}


@router.put("/", response_model=AdvertisementRead)
async def update_advertisement_endpoint(updated_advertisement: AdvertisementUpdate, user: User = Depends(current_user)) -> AdvertisementRead:
    """
    Asynchronously updates an existing advertisement.

    Args:
        updated_advertisement (AdvertisementUpdate): The updated advertisement data.
        user (User): The current user, required for authorization.

    Returns:
        AdvertisementRead: The updated advertisement.
    """
    logger.info(f"Update advertisement with id {updated_advertisement.id}")
    return await update_advertisement(updated_advertisement)