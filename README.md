# T-Bot

A comprehensive Django REST API project demonstrating advanced backend development skills including JWT authentication, Celery background tasks, PostgreSQL database, and interactive Telegram bot integration.

## 🚀 Features

### Core Features

- ✅ **Django REST Framework** with comprehensive API endpoints
- ✅ **JWT Authentication** with access/refresh token system
- ✅ **PostgreSQL Database** with optimized queries
- ✅ **Celery Background Tasks** with Redis broker
- ✅ **Interactive Telegram Bot** with inline keyboards
- ✅ **Email Integration** with Gmail SMTP
- ✅ **User Analytics & Tracking** system
- ✅ **Admin Dashboard** with advanced features

### Advanced Features

- 🎯 **Interactive Bot Menus** with callback handlers
- 📊 **Real-time User Statistics** and engagement metrics
- 📧 **Automated Email Notifications** for user registration
- 🔄 **Background Task Processing** with Celery Beat scheduling
- 📈 **User Interaction Tracking** and analytics
- 🛡️ **Production-ready Security** configurations
- 📱 **Responsive Admin Interface** with custom actions

## 🛠️ Tech Stack

| Component          | Technology            | Version |
| ------------------ | --------------------- | ------- |
| **Backend**        | Django                | 5.2.3   |
| **API Framework**  | Django REST Framework | Latest  |
| **Authentication** | JWT (Simple JWT)      | Latest  |
| **Database**       | PostgreSQL            | 15+     |
| **Task Queue**     | Celery + Redis        | Latest  |
| **Bot Framework**  | python-telegram-bot   | 20.7    |
| **Environment**    | environs              | 10.3.0  |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **PostgreSQL 12+**
- **Redis Server**
- **Git**
- **Telegram Account** (for bot setup)
- **Gmail Account** (for email features)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone
cd T-Bot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# PostgreSQL Database
POSTGRES_DB=internship_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here

# Email Configuration (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### 5. Database Setup

**Create PostgreSQL Database:**

```bash
# Access PostgreSQL shell
psql postgres

# Create database and user
CREATE DATABASE internship_db WITH TEMPLATE = template0;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE internship_db TO your_db_user;

# Exit PostgreSQL shell
\q
```

**Run Django Migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Telegram Bot Setup

**Create Telegram Bot:**

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the prompts to create your bot
4. Copy the bot token to your `.env` file

**Gmail App Password Setup:**

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security → App Passwords
3. Generate an app password for "Mail"
4. Use this password in your `.env` file

## 🚀 Running the Application

You need to run **4 separate processes** in different terminals:

### Terminal 1: Django Development Server

```bash
python manage.py runserver
```

### Terminal 2: Redis Server

```bash
redis-server
```

### Terminal 3: Celery Worker

```bash
celery -A internship_project worker --loglevel=info
```

### Terminal 4: Telegram Bot

```bash
python manage.py run_telegram_bot
```

### Optional: Celery Beat (for scheduled tasks)

```bash
celery -A internship_project beat --loglevel=info
```

### Optional: Flower (task monitoring)

```bash
pip install flower
celery -A internship_project flower
# Access at http://localhost:5555
```

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Public Endpoints

#### GET /api/public/

- **Description**: Public information endpoint
- **Authentication**: None required
- **Response**: General statistics and welcome message

```bash
curl -X GET http://localhost:8000/api/public/
```

### Authentication Endpoints

#### POST /api/register/

- **Description**: User registration
- **Authentication**: None required

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### POST /api/login/

- **Description**: User authentication
- **Authentication**: None required

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

#### POST /api/token/refresh/

- **Description**: Refresh JWT access token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your-refresh-token"}'
```

### Protected Endpoints

#### GET /api/protected/

- **Description**: Protected user information
- **Authentication**: JWT Token required

```bash
curl -X GET http://localhost:8000/api/protected/ \
  -H "Authorization: Bearer your-access-token"
```

#### GET /api/telegram-users/

- **Description**: List all registered Telegram users
- **Authentication**: JWT Token required

```bash
curl -X GET http://localhost:8000/api/telegram-users/ \
  -H "Authorization: Bearer your-access-token"
```

## 🤖 Telegram Bot Usage

### Available Commands

| Command  | Description                       | Example  |
| -------- | --------------------------------- | -------- |
| `/start` | Register account & show main menu | `/start` |
| `/help`  | Display help information          | `/help`  |

### Interactive Features

The bot provides an interactive menu system with inline keyboards:

- **📊 My Stats** - View your user statistics and engagement metrics
- **🔗 API Endpoints** - Get information about available API endpoints
- **📈 Bot Statistics** - Request detailed bot analytics
- **❓ Help** - Display comprehensive help information

### Bot Workflow

1. **User Registration**: Send `/start` to register your Telegram account
2. **Interactive Menu**: Use inline buttons to navigate features
3. **Statistics**: View personalized user analytics
4. **API Integration**: Access information about REST API endpoints

## 🔧 Admin Dashboard

Access the Django admin at: `http://localhost:8000/admin/`

### Admin Features

- **User Management**: View and manage registered users
- **Telegram Users**: Monitor bot user registrations and activity
- **User Profiles**: Link Django users with Telegram accounts
- **Analytics Dashboard**: View user engagement metrics
- **Bulk Actions**: Perform batch operations on users

## 📊 Background Tasks

### Automated Tasks

| Task                     | Trigger               | Description                              |
| ------------------------ | --------------------- | ---------------------------------------- |
| **Welcome Email**        | User Registration     | Sends welcome email with API information |
| **User Processing**      | Telegram Bot `/start` | Processes and logs new Telegram users    |
| **Analytics Generation** | On Demand             | Generates detailed user statistics       |

### Task Monitoring

Monitor background tasks using:

- **Celery Logs**: Check worker terminal output
- **Flower Dashboard**: Web-based task monitoring at `http://localhost:5555`
- **Django Admin**: View task results and user activities

## 🏗️ Project Structure

```
django_internship_assignment/
├── internship_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI application
│   ├── asgi.py                 # ASGI application
│   └── celery.py               # Celery configuration
├── main_app/                   # Main Django application
│   ├── migrations/             # Database migrations
│   ├── management/             # Custom management commands
│   │   └── commands/
│   │       └── run_telegram_bot.py
│   ├── models.py               # Database models
│   ├── views.py                # API views
│   ├── serializers.py          # DRF serializers
│   ├── urls.py                 # App URL patterns
│   ├── admin.py                # Admin configuration
│   ├── tasks.py                # Celery tasks
│   └── telegram_bot.py         # Telegram bot logic
├── templates/                  # HTML templates
│   └── registration/
│       └── login.html          # Login page
├── static/                     # Static files
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── manage.py                   # Django management script
└── README.md                   # This file
```

## 🧪 Testing

### API Testing Examples

**Test Public Endpoint:**

```bash
curl -X GET http://localhost:8000/api/public/
```

**Test User Registration:**

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apitest",
    "email": "apitest@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

**Test Protected Endpoint:**

```bash
# First login to get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "apitest", "password": "testpass123"}' | \
  python -c "import sys, json; print(json.load(sys.stdin)['tokens']['access'])")

# Use token for protected endpoint
curl -X GET http://localhost:8000/api/protected/ \
  -H "Authorization: Bearer $TOKEN"
```

### Bot Testing

1. Find your bot in Telegram using the username you created
2. Send `/start` command
3. Interact with the inline keyboard menu
4. Check Django admin for registered user data
5. Monitor Celery logs for background task execution

## 🚀 Production Deployment

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Production Database
POSTGRES_DB=prod_internship_db
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=secure-production-password
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432

# Production Redis
REDIS_URL=redis://your-redis-host:6379/0

# Email Configuration
EMAIL_HOST_USER=your-production-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Docker Deployment (Optional)

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/internship_db

  celery:
    build: .
    command: celery -A internship_project worker --loglevel=info
    depends_on:
      - db
      - redis

  bot:
    build: .
    command: python manage.py run_telegram_bot
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: internship_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass

  redis:
    image: redis:7-alpine
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error:**

```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Restart PostgreSQL
brew services restart postgresql
```

**Redis Connection Error:**

```bash
# Check Redis is running
redis-cli ping
# Should return "PONG"

# Start Redis if not running
redis-server
```

**Telegram Bot Not Responding:**

- Verify bot token in `.env` file
- Check bot management command is running
- Review bot logs for errors
- Ensure webhook is not set (for polling mode)

**Email Not Sending:**

- Verify Gmail app password (not regular password)
- Check 2FA is enabled on Gmail account
- Review email settings in Django settings

**Celery Tasks Not Processing:**

- Ensure Redis server is running
- Check Celery worker is active
- Review Celery logs for errors
- Verify task imports are correct

### Debug Mode

Enable detailed logging by adding to your `.env`:

```env
DEBUG=True
LOGGING_LEVEL=DEBUG
```

## 🙏 Acknowledgments

- Django REST Framework documentation
- python-telegram-bot library
- Celery documentation
- PostgreSQL community
- Redis community

**🎯 Project Highlights:**

- Production-ready Django REST API
- Interactive Telegram bot with advanced features
- Comprehensive background task system
- Real-time user analytics and tracking
- Professional admin dashboard
- Complete authentication system
- Email integration with automated notifications
- PostgreSQL database with optimized queries

This project demonstrates advanced Django development skills suitable for production environments and showcases modern backend development practices.
