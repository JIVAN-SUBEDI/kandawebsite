from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views import UserManagementViewSet, ProfileView, ChangePasswordView

router = DefaultRouter()
router.register("users", UserManagementViewSet, basename="users")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),

    path("profile/", ProfileView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),

    path("", include(router.urls)),
]