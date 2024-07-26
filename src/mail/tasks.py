import asyncio

from fastapi_mail import FastMail, MessageSchema

from tasks_celery import celery_app
from logger import celery_logger as logger
from mail.mail import mail_config

@celery_app.task
def send_email(subject: str, recipients: list[str], body: str):
    """
    Asynchronously sends an email to the specified recipients using FastMail within a Celery task.

    This function constructs an email message with the provided subject and body 
    and sends it to the list of recipients. In case of an error during the email 
    sending process, an error message will be logged.

    Args:
        subject (str): The subject of the email.
        recipients (list[str]): A list of email addresses to send the email to.
        body (str): The body of the email, formatted as HTML.
    
    Returns:
        None
    """
    logger.info(f"Sending email with subject {subject} to {recipients}")
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html"
    )

    fm = FastMail(mail_config)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(fm.send_message(message))
    except Exception as e:
        logger.error(f"Error sending email with subject {subject} to {recipients}: {e}")
