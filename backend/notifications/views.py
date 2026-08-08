from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trigger, NotificationTemplate, NotificationLog
from .serializers import (
    TriggerSerializer,
    NotificationTemplateSerializer,
    NotificationLogSerializer,
)


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


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer