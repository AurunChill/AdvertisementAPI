from mail.tasks import send_email
from user.models import User

async def send_email_verification_msg(user: User, verification_token: str):
    subject = "Verify your account"
    verify_link = f"http://localhost:8080/auth/verify-account?token={verification_token}"
    body = f"Hello {user.username}, use the following link to verify your account: {verify_link}"
    send_email.delay(subject, recipients=[user.email], body=body)