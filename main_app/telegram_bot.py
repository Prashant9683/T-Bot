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

@sync_to_async
def get_user_stats(telegram_user_id):
    """Get user statistics"""
    try:
        user = TelegramUser.objects.get(telegram_user_id=telegram_user_id)
        return {
            'username': user.telegram_username or 'Not set',
            'join_date': user.created_at.strftime('%Y-%m-%d'),
            'total_users': TelegramUser.objects.count(),
            'user_rank': list(TelegramUser.objects.order_by('created_at')).index(user) + 1
        }
    except TelegramUser.DoesNotExist:
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enhanced /start command with interactive menu"""
    user = update.effective_user
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    
    try:
        telegram_user, created = await save_telegram_user(user_data)
        display_name = user.first_name or user.username or f"User {user.id}"
        
        if created:
            message = f"""
🎉 Welcome to T-Bot!

Hello {display_name}! Your account has been registered.

📊 Your Details:
• Username: @{user.username or 'Not set'}
• Name: {user.first_name or ''} {user.last_name or ''}
• Telegram ID: {user.id}

Choose an option below:
"""
            process_telegram_user_data.delay(telegram_user.id)
        else:
            message = f"👋 Welcome back, {display_name}!\n\nChoose an option:"
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton("📊 My Stats", callback_data='stats')],
            [InlineKeyboardButton("🔗 API Endpoints", callback_data='endpoints')],
            [InlineKeyboardButton("📈 Bot Statistics", callback_data='bot_stats')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)
        logger.info(f"User @{user.username or user.id} used /start command")
        
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "Sorry, there was an error processing your request. Please try again later."
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'stats':
        stats = await get_user_stats(user_id)
        if stats:
            message = f"""
📊 Your Statistics:

👤 Username: @{stats['username']}
📅 Joined: {stats['join_date']}
🏆 User Rank: #{stats['user_rank']} of {stats['total_users']}
📈 Total Bot Users: {stats['total_users']}
"""
        else:
            message = "❌ Unable to fetch your statistics."
            
    elif query.data == 'endpoints':
        message = """
🔗 Available API Endpoints:

🌐 Public:
• GET /api/public/ - Public information

🔐 Authentication:
• POST /api/register/ - User registration
• POST /api/login/ - User login
• POST /api/token/refresh/ - Refresh JWT token

🛡️ Protected (requires JWT):
• GET /api/protected/ - Protected endpoint
• GET /api/telegram-users/ - List Telegram users

Base URL: http://localhost:8000
"""
    
    elif query.data == 'bot_stats':
        # Trigger async task to generate bot stats
        generate_user_stats.delay(user_id)
        message = "📈 Generating bot statistics... You'll receive them shortly!"
        
    elif query.data == 'help':
        message = """
🤖 T-Bot

Available commands:
• /start - Main menu
• /help - Show this help
• /broadcast - Send message to all users (admin only)

This bot demonstrates:
✅ Django REST Framework
✅ JWT Authentication  
✅ Celery Background Tasks
✅ PostgreSQL Database
✅ Interactive Telegram Bot
"""
    
    # Back button for navigation
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def back_to_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle back to menu button"""
    query = update.callback_query
    await query.answer()
    
    # Recreate main menu
    keyboard = [
        [InlineKeyboardButton("📊 My Stats", callback_data='stats')],
        [InlineKeyboardButton("🔗 API Endpoints", callback_data='endpoints')],
        [InlineKeyboardButton("📈 Bot Statistics", callback_data='bot_stats')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = "🏠 Main Menu - Choose an option:"
    await query.edit_message_text(message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command
    """
    help_text = """
🤖 T-Bot

Available commands:
• /start - Register your Telegram account
• /help - Show this help message

This bot demonstrates:
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
