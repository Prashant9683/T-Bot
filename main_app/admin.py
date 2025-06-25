from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import TelegramUser, UserProfile, BotInteraction, BroadcastMessage

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_username', 'full_name', 'telegram_user_id', 'is_active', 'days_since_joined', 'last_interaction', 'interaction_count')
    list_filter = ('is_active', 'created_at', 'last_interaction')
    search_fields = ('telegram_username', 'first_name', 'last_name', 'telegram_user_id')
    readonly_fields = ('created_at', 'days_since_joined', 'interaction_count')
    list_per_page = 25
    
    def interaction_count(self, obj):
        count = BotInteraction.objects.filter(telegram_user=obj).count()
        return count
    interaction_count.short_description = 'Interactions'
    
    def days_since_joined(self, obj):
        return obj.days_since_joined
    days_since_joined.short_description = 'Days Active'
    
    actions = ['mark_as_inactive', 'mark_as_active']
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_as_inactive.short_description = "Mark selected users as inactive"
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_as_active.short_description = "Mark selected users as active"

@admin.register(BotInteraction)
class BotInteractionAdmin(admin.ModelAdmin):
    list_display = ('telegram_user', 'interaction_type', 'command_or_data', 'timestamp')
    list_filter = ('interaction_type', 'timestamp')
    search_fields = ('telegram_user__telegram_username', 'command_or_data')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_sent', 'delivery_stats')
    list_filter = ('is_sent', 'created_at')
    search_fields = ('title', 'message')
    readonly_fields = ('created_at', 'sent_at', 'total_recipients', 'successful_sends', 'failed_sends')
    
    def delivery_stats(self, obj):
        if obj.is_sent:
            return format_html(
                '<span style="color: green;">✅ {}/{} delivered</span>',
                obj.successful_sends,
                obj.total_recipients
            )
        return format_html('<span style="color: orange;">⏳ Pending</span>')
    delivery_stats.short_description = 'Delivery Status'
    
    actions = ['send_broadcast']
    
    def send_broadcast(self, request, queryset):
        from .tasks import broadcast_message_to_users
        for broadcast in queryset.filter(is_sent=False):
            broadcast_message_to_users.delay(broadcast.id)
        self.message_user(request, f"Broadcasting {queryset.count()} messages...")
    send_broadcast.short_description = "Send selected broadcasts"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
