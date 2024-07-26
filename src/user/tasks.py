from uuid import UUID
import asyncio

from tasks_celery import celery_app
from logger import celery_logger as logger

from user.service import delete_user_verification_token


@celery_app.task
def delete_user_verification_token_task(user_id: UUID):
    """
    Celery task to delete the verification token for a specified user.

    This task is run asynchronously and logs the deletion of the verification 
    token for the given user ID. It utilizes asyncio to perform the deletion 
    operation.

    Args:
        user_id (UUID): The unique identifier of the user for whom the 
                        verification token will be deleted.
    """
    logger.info(f"Deleting verification token for user {user_id}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_user_verification_token(user_id))
