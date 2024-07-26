from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select

from user.models import User
from user.schemas import UserUpdate, UserRead
from logger import db_query_logger as logger
from db import async_session_maker


async def get_user_by_username(username: str) -> Optional[UserRead]:
    """Get user by username"""
    async with async_session_maker() as session:
        query = select(User).where(username == User.username)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        return user
    

async def get_user_by_email(email: str) -> Optional[UserRead]:
    """Get user by email"""
    async with async_session_maker() as session:
        query = select(User).where(email == User.email)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        return user
    

async def delete_user(user: User):
    """Delete user"""
    async with async_session_maker() as session:
        stmt = select(User).where(User.id == user.id)
        result = await session.execute(stmt)
        db_user = result.unique().scalar_one_or_none()
        await session.refresh(db_user)
        await session.delete(db_user)
        await session.commit()
        logger.info(f"User {db_user} deleted")


async def update_user(user: User, updated_user: UserUpdate) -> UserRead:
    """Update user"""
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
    """Update user verification token"""
    async with async_session_maker() as session:
        query = select(User).where(user_id == User.id)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        user.verification_token = token
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    

async def delete_user_verification_token(user_id: UUID) -> Optional[User]:
    """Delete user verification token"""
    async with async_session_maker() as session:
        query = select(User).where(user_id == User.id)
        user = (await session.execute(query)).unique().scalar_one_or_none()
        user.verification_token = None
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    

async def verify_verification_token(token: str) -> Optional[User]:
    """Verify user verification token"""
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