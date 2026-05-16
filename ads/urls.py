from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicAdViewSet, AdminAdViewSet

router = DefaultRouter()
router.register("public", PublicAdViewSet, basename="public-ads")
router.register("admin", AdminAdViewSet, basename="admin-ads")

urlpatterns = [
    path("", include(router.urls)),
]