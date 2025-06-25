from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Public endpoints
    path('public/', views.public_endpoint, name='public_endpoint'),
    
    # Authentication endpoints
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Protected endpoints
    path('protected/', views.protected_endpoint, name='protected_endpoint'),
    path('telegram-users/', views.telegram_users_list, name='telegram_users_list'),
]
