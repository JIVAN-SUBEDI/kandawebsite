from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicCommentViewSet, AdminCommentViewSet

router = DefaultRouter()
router.register("public", PublicCommentViewSet, basename="public-comments")
router.register("admin", AdminCommentViewSet, basename="admin-comments")

urlpatterns = [
path("", include(router.urls)),
]