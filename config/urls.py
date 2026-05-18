from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [

    path("api/auth/", include("accounts.urls")),
    path("api/videos/", include("videos.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/ads/", include("ads.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += [
    re_path(
        r"^(?!api/|media/|static/).*$",
        TemplateView.as_view(template_name="index.html"),
    ),
]