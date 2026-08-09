from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trigger, NotificationTemplate, NotificationLog
from .serializers import (
    TriggerSerializer,
    NotificationTemplateSerializer,
    NotificationLogSerializer,
)
from .services.notification_service import NotificationService
from django.contrib.auth import get_user_model

User = get_user_model()

class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer

    @action(detail=True, methods=["patch"])
    def toggle(self, request, pk=None):
        template = self.get_object()

        template.is_enabled = not template.is_enabled
        template.save()

        return Response(
            {
                "id": template.id,
                "is_enabled": template.is_enabled,
                "message": (
                    "Template enabled"
                    if template.is_enabled
                    else "Template disabled"
                ),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="test-send")
    def test_send(self, request, pk=None):
        template = self.get_object()

        if not template.is_enabled:
            return Response(
                {"error": "Template is disabled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.first()

        if not user:
            return Response(
                {"error": "No test user available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = NotificationService()

        try:
            result = service.send(template, user)

            NotificationLog.objects.create(
                user=user,
                trigger=template.trigger,
                channel=template.channel,
                status="SUCCESS",
                response=str(result),
            )

        except Exception as e:
            NotificationLog.objects.create(
                user=user,
                trigger=template.trigger,
                channel=template.channel,
                status="FAILED",
                response=str(e),
            )

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Test notification sent successfully",
                "result": result,
            },
            status=status.HTTP_200_OK,
        )
class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer