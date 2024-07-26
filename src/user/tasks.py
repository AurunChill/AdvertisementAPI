from uuid import UUID
import asyncio

from tasks_celery import celery_app
from logger import celery_logger as logger

from user.service import delete_user_verification_token


@celery_app.task
def delete_user_verification_token_task(user_id: UUID):
    logger.info(f"Deleting verification token for user {user_id}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_user_verification_token(user_id))