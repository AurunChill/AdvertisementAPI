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
async def read_advertisements(user: User = Depends(current_user)):
    """Get all advertisements"""
    logger.info("Get all advertisements")
    return await get_advertisements_all()


@router.get("/{advertisement_id}", response_model=AdvertisementRead)
async def read_advertisement_by_id(advertisement_id: int, user: User = Depends(current_user)):
    """Get advertisement by id"""
    logger.info(f"Get advertisement with id {advertisement_id}")
    advertisement = await get_advertisement_by_id(advertisement_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AdvertisementRead)
async def create_advertisement_endpoint(new_advertisement: AdvertisementCreate, user: User = Depends(current_user)):
    """Create a new advertisement"""
    logger.info("Create new advertisement")
    return await create_advertisement(new_advertisement)


@router.delete("/{advertisement_id}")
async def delete_advertisement_endpoint(advertisement_id: int, user: User = Depends(current_user)):
    """Delete advertisement."""
    logger.info(f"Delete advertisement with id {advertisement_id}") 
    result = await delete_advertisement(advertisement_id)
    if not result:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return {"detail": "Advertisement deleted"}


@router.put("/", response_model=AdvertisementRead)
async def update_advertisement_endpoint(updated_advertisement: AdvertisementUpdate, user: User = Depends(current_user)):
    """Update advertisement."""
    logger.info(f"Update advertisement with id {updated_advertisement.id}")
    return await update_advertisement(updated_advertisement)
