from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select

from user.models import User
from user.schemas import UserUpdate, UserRead
from logger import db_query_logger as logger
from db import async_session_maker


async def get_user_by_username(username: str) -> Optional[UserRead]:
    """
    Asynchronously retrieves a user by their username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        Optional[UserRead]: The user object corresponding to the username, 
                            or None if no user is found.
    """
    async with async_session_maker() as session:
        query = select(User).where(username == User.username)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        return user
    

async def get_user_by_email(email: str) -> Optional[UserRead]:
    """
    Asynchronously retrieves a user by their email address.

    Args:
        email (str): The email address of the user to retrieve.

    Returns:
        Optional[UserRead]: The user object corresponding to the email, 
                            or None if no user is found.
    """
    async with async_session_maker() as session:
        query = select(User).where(email == User.email)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        return user
    

async def delete_user(user: User):
    """
    Asynchronously deletes a specified user from the database.

    Args:
        user (User): The user object to be deleted.

    Raises:
        Exception: If the user is not found, an exception will be raised.

    Returns:
        None
    """
    async with async_session_maker() as session:
        stmt = select(User).where(User.id == user.id)
        result = await session.execute(stmt)
        db_user = result.unique().scalar_one_or_none()
        await session.refresh(db_user)
        await session.delete(db_user)
        await session.commit()
        logger.info(f"User {db_user} deleted")


async def update_user(user: User, updated_user: UserUpdate) -> UserRead:
    """
    Asynchronously updates a user's details in the database.

    Args:
        user (User): The user object containing the current user's details.
        updated_user (UserUpdate): An object containing the updated user information.

    Raises:
        HTTPException: If the user is not found, raises a 404 error.

    Returns:
        UserRead: The updated user object.
    """
    async with async_session_maker() as session:
        query = select(User).where(User.id == user.id)
        db_user = (await session.execute(query)).unique().scalar_one_or_none()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


async def update_user_verification_token(user_id: UUID, token: str) -> Optional[User]:
    """
    Asynchronously updates a user's verification token.

    Args:
        user_id (UUID): The unique identifier of the user.
        token (str): The new verification token to set for the user.

    Returns:
        Optional[User]: The user object with the updated verification token, 
                        or None if the user is not found.
    """
    async with async_session_maker() as session:
        query = select(User).where(user_id == User.id)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        user.verification_token = token
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    

async def delete_user_verification_token(user_id: UUID) -> Optional[User]:
    """
    Asynchronously deletes the verification token for a specified user.

    Args:
        user_id (UUID): The unique identifier of the user.

    Returns:
        Optional[User]: The user object with the verification token set to None, 
                        or None if the user is not found.
    """
    async with async_session_maker() as session:
        query = select(User).where(user_id == User.id)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        user.verification_token = None
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    

async def verify_verification_token(token: str) -> Optional[User]:
    """
    Asynchronously verifies a user's verification token.

    Args:
        token (str): The verification token to check.

    Returns:
        Optional[User]: The user object if the verification token is valid, 
                        or raises an HTTPException if not found.

    Raises:
        HTTPException: If the verification token is not valid or not found.
    """
    async with async_session_maker() as session:
        query = select(User).where(token == User.verification_token)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        if not user:
            logger.warning(f"User with verification token {token} not found")
            raise HTTPException(status_code=404, detail=f"User with this verification token {token} not found")

        logger.debug(f"User with verification token {token} verified")
        user.is_verified = True
        user.verification_token = None
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user