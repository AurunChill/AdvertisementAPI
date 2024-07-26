from fastapi import HTTPException
from sqlalchemy import select

from db import async_session_maker
from advertisement.models import Advertisement
from advertisement.schemas import AdvertisementCreate, AdvertisementRead, AdvertisementUpdate
from logger import db_query_logger as logger


async def get_advertisements_all() -> list[AdvertisementRead]:
    """
    Retrieves all advertisements from the database.

    Returns:
        list[AdvertisementRead]: A list of AdvertisementRead objects representing all the advertisements in the database.
    """
    async with async_session_maker() as session:
        advertisements = await session.execute(select(Advertisement))
        return advertisements.scalars().all()


async def get_advertisement_by_id(advertisement_id: int) -> AdvertisementRead:
    """
    Asynchronously retrieves an advertisement by its ID.

    Args:
        advertisement_id (int): The ID of the advertisement to retrieve.

    Raises:
        HTTPException: If no advertisement is found with the given ID, a 404 error is raised.

    Returns:
        AdvertisementRead: The advertisement object corresponding to the provided ID.
    """
    async with async_session_maker() as session:
        advertisement = await session.get(Advertisement, advertisement_id)

        if not advertisement:
            logger.warning(f"Advertisement with id {advertisement_id} not found")
            raise HTTPException(status_code=404, detail="Advertisement not found")

        return advertisement


async def create_advertisement(new_advertisement: AdvertisementCreate):
    """
    Asynchronously creates a new advertisement.

    Args:
        new_advertisement (AdvertisementCreate): The data for the advertisement to create.

    Returns:
        Advertisement: The created advertisement object.
    """
    async with async_session_maker() as session:
        new_advertisement_data = new_advertisement.model_dump()
        advertisement = Advertisement(**new_advertisement_data)
        session.add(advertisement)
        await session.commit()
        return advertisement
    

async def delete_advertisement(advertisement_id: int):
    """
    Asynchronously deletes an advertisement by its ID.

    Args:
        advertisement_id (int): The ID of the advertisement to delete.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    async with async_session_maker() as session:
        advertisement = await session.get(Advertisement, advertisement_id)

        if advertisement is None:
            raise HTTPException(status_code=404, detail=f"Advertisement with id {advertisement_id} not found")
        
        await session.delete(advertisement)
        await session.commit()
        return {"status": f"Advertisement with id {advertisement.id} deleted successfully"}


async def update_advertisement(updated_advertisement: AdvertisementUpdate) -> AdvertisementRead:
    """
    Asynchronously updates an existing advertisement.

    Args:
        updated_advertisement (AdvertisementUpdate): The updated data for the advertisement.

    Raises:
        HTTPException: If the advertisement to update is not found.

    Returns:
        AdvertisementRead: The updated advertisement object.
    """
    async with async_session_maker() as session:
        advertisement = await get_advertisement_by_id(updated_advertisement.id)
        updated_data = updated_advertisement.model_dump(exclude_unset=True)
        
        # Update the advertisement's attributes with new values
        for key, value in updated_data.items():
            setattr(advertisement, key, value)
        
        session.add(advertisement)
        await session.commit()
        await session.refresh(advertisement)
        return advertisement
