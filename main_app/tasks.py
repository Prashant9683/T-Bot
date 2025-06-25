from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to newly registered user
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Welcome to Django Internship Assignment!'
        message = f'''
        Hello {user.first_name or user.username},
        
        Welcome to our Django Internship Assignment platform!
        
        Your account has been successfully created.
        
        Username: {user.username}
        Email: {user.email}
        
        You can now access our protected endpoints using JWT authentication.
        
        Best regards,
        Django Internship Team
        '''
        
        send_mail(
            subject,
            message,
            'noreply@internship.com',
            [user.email],
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent to {user.email}")
        return f"Welcome email sent to {user.email}"
        
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist")
        return f"User with id {user_id} does not exist"
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return f"Error sending email: {str(e)}"

@shared_task
def process_telegram_user_data(telegram_user_id):
    """
    Process telegram user data in background
    """
    try:
        from .models import TelegramUser
        telegram_user = TelegramUser.objects.get(id=telegram_user_id)
        

        logger.info(f"Processing data for telegram user: @{telegram_user.telegram_username}")
        

        return f"Processed data for @{telegram_user.telegram_username}"
        
    except Exception as e:
        logger.error(f"Error processing telegram user data: {str(e)}")
        return f"Error: {str(e)}"
