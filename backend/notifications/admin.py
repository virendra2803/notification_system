from django.contrib import admin
from .models import Trigger, NotificationTemplate, NotificationLog

# Register your models here.
@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "trigger",
        "channel",
        "is_enabled",
        "created_at",
    )
    list_filter = ("channel", "is_enabled")
    search_fields = ("trigger__name",)


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "trigger",
        "channel",
        "status",
        "sent_at",
    )
    list_filter = ("channel", "status")
    search_fields = ("user__username",)