from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from .models import TelegramUser, UserProfile
from .serializers import UserRegistrationSerializer, TelegramUserSerializer, PublicDataSerializer
from .tasks import send_welcome_email

@api_view(['GET'])
@permission_classes([AllowAny])
def public_endpoint(request):
    """
    Public endpoint accessible to everyone
    """
    data = {
        'message': 'Welcome to our T-Bot API!',
        'timestamp': timezone.now(),
        'total_users': User.objects.count(),
    }
    serializer = PublicDataSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    """
    Protected endpoint accessible only to authenticated users
    """
    user_profile = UserProfile.objects.get(user=request.user)
    telegram_info = None
    
    if user_profile.telegram_user:
        telegram_info = TelegramUserSerializer(user_profile.telegram_user).data
    
    data = {
        'message': f'Hello {request.user.username}! This is a protected endpoint.',
        'user_info': {
            'username': request.user.username,
            'email': request.user.email,
            'date_joined': request.user.date_joined,
        },
        'telegram_info': telegram_info,
        'timestamp': timezone.now(),
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    User registration endpoint
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Send welcome email asynchronously
        send_welcome_email.delay(user.id)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully!',
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    User login endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful!',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def telegram_users_list(request):
    """
    List all telegram users (protected endpoint)
    """
    telegram_users = TelegramUser.objects.all()
    serializer = TelegramUserSerializer(telegram_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bot_analytics(request):
    """Get bot analytics (admin only)"""
    if not request.user.is_staff:
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    from .models import BotInteraction
    from django.db.models import Count
    from datetime import timedelta
    
    # Calculate analytics
    total_users = TelegramUser.objects.count()
    active_users_week = TelegramUser.objects.filter(
        last_interaction__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    total_interactions = BotInteraction.objects.count()
    interactions_today = BotInteraction.objects.filter(
        timestamp__date=timezone.now().date()
    ).count()
    
    # Most popular commands
    popular_commands = BotInteraction.objects.filter(
        interaction_type='command'
    ).values('command_or_data').annotate(
        count=Count('command_or_data')
    ).order_by('-count')[:5]
    
    data = {
        'total_users': total_users,
        'active_users_week': active_users_week,
        'total_interactions': total_interactions,
        'interactions_today': interactions_today,
        'popular_commands': list(popular_commands),
        'engagement_rate': round((active_users_week / max(total_users, 1)) * 100, 2)
    }
    
    return Response(data, status=status.HTTP_200_OK)
