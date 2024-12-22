from django.core.mail import EmailMessage, BadHeaderError
from core.models import User
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def account_created_task(user_id):
    user = User.objects.get(pk=user_id)
    message = f"""
    <html>
        <body>
            <h2 style="color: #333;">Welcome to Todoey, {user.username}!</h2>
            <p>We are excited to have you on board. Your account has been created successfully.</p>
            <p>Thank you for choosing us.</p>
            <p>Regards,<br>Todoey CEO</p>
            <img src="https://images.unsplash.com/photo-1641261689141-ee46b8a0470c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Welcome Image" style="width:100%; max-width:600px;">
        </body>
    </html>
    """

    try:
        mail = EmailMessage(
            'Welcome to Todoey',
            message,
            'aaronpinto111@gmail.com',
            [user.email],
        )
        mail.content_subtype = 'html'
        mail.send()
    except BadHeaderError as e:
        logger.error(f"Error - failed to send mail to {user.email}- {e}")
        return False