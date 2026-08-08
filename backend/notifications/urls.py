from rest_framework.routers import DefaultRouter
from .views import (
    TriggerViewSet,
    NotificationTemplateViewSet,
    NotificationLogViewSet,
)

router = DefaultRouter()

router.register("triggers", TriggerViewSet)
router.register("templates", NotificationTemplateViewSet)
router.register("logs", NotificationLogViewSet)

urlpatterns = router.urls