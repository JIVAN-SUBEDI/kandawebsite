from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicVideoViewSet, AdminVideoViewSet

router = DefaultRouter()
router.register("public", PublicVideoViewSet, basename="public-videos")
router.register("admin", AdminVideoViewSet, basename="admin-videos")

urlpatterns = [
    path("", include(router.urls)),
]