from django.contrib import admin
from .models import TelegramUser, UserProfile

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_username', 'first_name', 'last_name', 'telegram_user_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('telegram_username', 'first_name', 'last_name')
    readonly_fields = ('created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
