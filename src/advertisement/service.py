from fastapi import HTTPException
from sqlalchemy import select

from db import async_session_maker
from advertisement.models import Advertisement
from advertisement.schemas import AdvertisementCreate, AdvertisementRead, AdvertisementUpdate
from logger import db_query_logger as logger


async def get_advertisements_all() -> list[AdvertisementRead]:
    """Get all advertisements"""
    async with async_session_maker() as session:
        advertisements = await session.execute(select(Advertisement))
        return advertisements.scalars().all()


async def get_advertisement_by_id(advertisement_id: int) -> AdvertisementRead:
    """Get an advertisement by advertisement_id"""
    async with async_session_maker() as session:
        advertisement = await session.get(Advertisement, advertisement_id)

        if not advertisement:
            logger.warning(f"Advertisement with id {advertisement_id} not found")
            raise HTTPException(status_code=404, detail="Advertisement not found")

        return advertisement


async def create_advertisement(new_advertisement: AdvertisementCreate):
    """Create a new advertisement"""
    async with async_session_maker() as session:
        new_advertisement_data = new_advertisement.model_dump()
        advertisement = Advertisement(**new_advertisement_data)
        session.add(advertisement)
        await session.commit()
        return advertisement
    

async def delete_advertisement(advertisement_id: int):
    """Delete advertisement with id advertisement_id"""
    async with async_session_maker() as session:
        advertisement = await session.get(Advertisement, advertisement_id)
        await session.delete(advertisement)
        await session.commit()
        return {"status": f"Advertisement with id {advertisement.id} deleted successfully"}


async def update_advertisement(updated_advertisement: AdvertisementUpdate) -> AdvertisementRead:
    """Update advertisement with updated_advertisement"""
    async with async_session_maker() as session:
        advertisement = await get_advertisement_by_id(updated_advertisement.id)
        updated_data = updated_advertisement.model_dump(exclude_unset=True)
        
        for key, value in updated_data.items():
            setattr(advertisement, key, value)
        
        session.add(advertisement)
        await session.commit()
        await session.refresh(advertisement)
        return advertisement
