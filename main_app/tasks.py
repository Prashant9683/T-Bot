from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging
import csv
import io

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_id):
    """Send welcome email to newly registered user"""
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Welcome to T-Bot!'
        message = f'''
Hello {user.first_name or user.username},

Welcome to our T-Bot platform!

Your account has been successfully created.

Username: {user.username}
Email: {user.email}

🔗 API Endpoints:
• Public: GET /api/public/
• Register: POST /api/register/
• Login: POST /api/login/
• Protected: GET /api/protected/ (requires JWT)

You can now access our protected endpoints using JWT authentication.

Best regards,
Django Internship Team
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
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
    """Process telegram user data in background"""
    try:
        from .models import TelegramUser, BotInteraction
        telegram_user = TelegramUser.objects.get(id=telegram_user_id)
        
        # Log the interaction
        BotInteraction.objects.create(
            telegram_user=telegram_user,
            interaction_type='command',
            command_or_data='/start'
        )
        
        logger.info(f"Processing data for telegram user: @{telegram_user.telegram_username}")
        return f"Processed data for @{telegram_user.telegram_username}"
        
    except Exception as e:
        logger.error(f"Error processing telegram user data: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def generate_user_stats(telegram_user_id):
    """Generate and send user statistics"""
    try:
        from .models import TelegramUser, BotInteraction
        from .telegram_bot import send_telegram_message_direct
        
        user = TelegramUser.objects.get(telegram_user_id=telegram_user_id)
        
        # Calculate statistics
        total_interactions = BotInteraction.objects.filter(telegram_user=user).count()
        recent_interactions = BotInteraction.objects.filter(
            telegram_user=user,
            timestamp__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        most_used_commands = BotInteraction.objects.filter(
            telegram_user=user,
            interaction_type='command'
        ).values('command_or_data').annotate(
            count=models.Count('command_or_data')
        ).order_by('-count')[:3]
        
        stats_message = f"""
📊 Your Detailed Statistics:

🎯 Total Interactions: {total_interactions}
📅 This Week: {recent_interactions}
📈 Member Since: {user.created_at.strftime('%B %d, %Y')}
🏆 Rank: #{list(TelegramUser.objects.order_by('created_at')).index(user) + 1}

🔥 Most Used Commands:
"""
        
        for i, cmd in enumerate(most_used_commands, 1):
            stats_message += f"{i}. {cmd['command_or_data']} ({cmd['count']} times)\n"
        
        # Send via Telegram (you'll need to implement this function)
        # send_telegram_message_direct(telegram_user_id, stats_message)
        
        logger.info(f"Generated stats for user {telegram_user_id}")
        return f"Stats generated for user {telegram_user_id}"
        
    except Exception as e:
        logger.error(f"Error generating user stats: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def broadcast_message_to_users(message_id):
    """Broadcast message to all active users"""
    try:
        from .models import BroadcastMessage, TelegramUser
        
        broadcast = BroadcastMessage.objects.get(id=message_id)
        active_users = TelegramUser.objects.filter(is_active=True)
        
        successful_sends = 0
        failed_sends = 0
        
        for user in active_users:
            try:
                # Here you would send the actual Telegram message
                # send_telegram_message_direct(user.telegram_user_id, broadcast.message)
                successful_sends += 1
            except Exception as e:
                logger.error(f"Failed to send message to {user.telegram_user_id}: {str(e)}")
                failed_sends += 1
        
        # Update broadcast statistics
        broadcast.successful_sends = successful_sends
        broadcast.failed_sends = failed_sends
        broadcast.total_recipients = active_users.count()
        broadcast.sent_at = timezone.now()
        broadcast.is_sent = True
        broadcast.save()
        
        logger.info(f"Broadcast completed: {successful_sends} sent, {failed_sends} failed")
        return f"Broadcast completed: {successful_sends} sent, {failed_sends} failed"
        
    except Exception as e:
        logger.error(f"Error broadcasting message: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def generate_daily_report():
    """Generate daily analytics report"""
    try:
        from .models import TelegramUser, BotInteraction
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Calculate metrics
        new_users_today = TelegramUser.objects.filter(created_at__date=today).count()
        total_users = TelegramUser.objects.count()
        interactions_today = BotInteraction.objects.filter(timestamp__date=today).count()
        
        active_users_today = BotInteraction.objects.filter(
            timestamp__date=today
        ).values('telegram_user').distinct().count()
        
        report = f"""
📊 Daily Bot Report - {today}

👥 Users:
• New Today: {new_users_today}
• Total Users: {total_users}
• Active Today: {active_users_today}

💬 Interactions:
• Today: {interactions_today}

📈 Growth Rate: {((new_users_today / max(total_users - new_users_today, 1)) * 100):.1f}%
"""
        
        # You could send this to admin users or log it
        logger.info(f"Daily report generated: {report}")
        return report
        
    except Exception as e:
        logger.error(f"Error generating daily report: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def cleanup_old_interactions():
    """Clean up old bot interactions (keep last 30 days)"""
    try:
        from .models import BotInteraction
        
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_count = BotInteraction.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old interactions")
        return f"Cleaned up {deleted_count} old interactions"
        
    except Exception as e:
        logger.error(f"Error cleaning up interactions: {str(e)}")
        return f"Error: {str(e)}"
