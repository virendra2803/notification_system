from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Trigger(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NotificationTemplate(models.Model):

    CHANNEL_CHOICES = [
        ("EMAIL", "Email"),
        ("WHATSAPP", "WhatsApp"),
        ("WEB_PUSH", "Web Push"),
    ]

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.CASCADE,
        related_name="templates"
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES
    )

    subject = models.CharField(
        max_length=255,
        blank=True
    )

    body = models.TextField()

    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("trigger", "channel")

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"

class NotificationLog(models.Model):

    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.CASCADE
    )

    channel = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    response = models.TextField(blank=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.trigger.name} - {self.channel}"