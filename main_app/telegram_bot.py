import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from django.conf import settings
from asgiref.sync import sync_to_async
from .models import TelegramUser
from .tasks import process_telegram_user_data

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@sync_to_async
def save_telegram_user(user_data):
    """
    Save telegram user to database with proper null handling
    """
    telegram_user, created = TelegramUser.objects.get_or_create(
        telegram_user_id=user_data['id'],
        defaults={
            'telegram_username': user_data.get('username') or '',
            'first_name': user_data.get('first_name') or '',
            'last_name': user_data.get('last_name') or '',
        }
    )
    
    if not created:
        # Update existing user data
        telegram_user.telegram_username = user_data.get('username') or telegram_user.telegram_username or ''
        telegram_user.first_name = user_data.get('first_name') or telegram_user.first_name or ''
        telegram_user.last_name = user_data.get('last_name') or telegram_user.last_name or ''
        telegram_user.save()
    
    return telegram_user, created

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command with proper null value handling
    """
    user = update.effective_user
    
    # Prepare user data with fallbacks for missing values
    user_data = {
        'id': user.id,
        'username': user.username,  # Can be None
        'first_name': user.first_name,  # Can be None
        'last_name': user.last_name,  # Can be None
    }
    
    try:
        # Save user to database
        telegram_user, created = await save_telegram_user(user_data)
        
        # Create display name with fallbacks
        display_name = user.first_name or user.username or f"User {user.id}"
        username_display = f"@{user.username}" if user.username else "No username set"
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Name not set"
        
        if created:
            message = f"""
🎉 Welcome to Django Internship Assignment Bot!

Hello {display_name}!

Your Telegram account has been successfully registered in our system.

📊 Your Details:
• Username: {username_display}
• Name: {full_name}
• Telegram ID: {user.id}

You can now use our Django API endpoints with your account!

🔗 Available endpoints:
• Public API: GET /api/public/
• Protected API: GET /api/protected/ (requires authentication)
• Register: POST /api/register/
• Login: POST /api/login/

Thank you for joining us! 🚀
            """
            

            from .tasks import process_telegram_user_data
            process_telegram_user_data.delay(telegram_user.id)
            
        else:
            message = f"""
👋 Welcome back, {display_name}!

Your account is already registered in our system.

You can continue using our Django API endpoints.
            """
        
        await update.message.reply_text(message)
        logger.info(f"User @{user.username or user.id} used /start command")
        
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "Sorry, there was an error processing your request. Please try again later."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command
    """
    help_text = """
🤖 Django Internship Assignment Bot

Available commands:
• /start - Register your Telegram account
• /help - Show this help message

This bot is part of a Django internship assignment that demonstrates:
✅ Django REST Framework
✅ JWT Authentication
✅ Celery Background Tasks
✅ Telegram Bot Integration
✅ Production-ready code structure

For more information, check out the API documentation!
    """
    
    await update.message.reply_text(help_text)

def run_telegram_bot():
    """
    Run the telegram bot
    """
    # Create the Application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Run the bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    run_telegram_bot()
