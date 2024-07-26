from mail.tasks import send_email
from user.models import User

async def send_email_verification_msg(user: User, verification_token: str):
    """
    Asynchronously sends an email verification message to the given user.

    Args:
        user (User): The user to send the verification email to.
        verification_token (str): The verification token for the user.

    Returns:
        None
    """
    subject = "Verify your account"
    verify_link = f"http://localhost:8080/auth/verify-account?token={verification_token}"
    body = f"Hello {user.username}, use the following link to verify your account: {verify_link}"
    send_email.delay(subject, recipients=[user.email], body=body)