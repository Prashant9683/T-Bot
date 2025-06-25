from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect


def home_view(request):
    """Home page view"""
    return HttpResponse("""
    <h1>T-Bot</h1>
    <h2>Welcome to the API!</h2>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/public/">Public API</a></li>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/login/">Login</a></li>
    </ul>
    <p>API Documentation:</p>
    <ul>
        <li>POST /api/register/ - User registration</li>
        <li>POST /api/login/ - User login</li>
        <li>GET /api/protected/ - Protected endpoint (requires JWT)</li>
        <li>GET /api/telegram-users/ - List Telegram users (requires JWT)</li>
    </ul>
    """)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('main_app.urls')),
    
    # Django Login for web-based access
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
