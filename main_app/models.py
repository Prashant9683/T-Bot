from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TelegramUser(models.Model):
    telegram_username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    telegram_user_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"@{self.telegram_username or 'No Username'}"
    
    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or "No name"
    
    @property
    def days_since_joined(self):
        return (timezone.now() - self.created_at).days

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class BotInteraction(models.Model):
    INTERACTION_TYPES = [
        ('command', 'Command'),
        ('callback', 'Callback'),
        ('message', 'Message'),
    ]
    
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    command_or_data = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.telegram_user} - {self.command_or_data}"

class BroadcastMessage(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    total_recipients = models.IntegerField(default=0)
    successful_sends = models.IntegerField(default=0)
    failed_sends = models.IntegerField(default=0)
    is_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
