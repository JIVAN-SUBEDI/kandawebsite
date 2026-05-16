from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.permissions import IsAdminOrStaffRole
from analytics.models import ActivityLog
from .models import Ad
from .serializers import AdSerializer

def get_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0]
    return request.META.get("REMOTE_ADDR")

class PublicAdViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        ad_type = self.request.query_params.get("type")
        qs = Ad.objects.filter(is_active=True)
        if ad_type:
            qs = qs.filter(ad_type=ad_type)
        return qs.order_by("-created_at")

    @action(detail=True, methods=["post"])
    def impression(self, request, pk=None):
        ad = self.get_object()
        ActivityLog.objects.create(
            action=ActivityLog.Action.AD_IMPRESSION,
            ad=ad,
            ip_address=get_ip(request)
        )
        return Response({"message": "Impression tracked."})

    @action(detail=True, methods=["post"])
    def click(self, request, pk=None):
        ad = self.get_object()
        ActivityLog.objects.create(
            action=ActivityLog.Action.AD_CLICK,
            ad=ad,
            ip_address=get_ip(request)
        )
        return Response({"message": "Click tracked."})

class AdminAdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by("-created_at")
    serializer_class = AdSerializer
    permission_classes = [IsAdminOrStaffRole]

    @action(detail=True, methods=["post"])
    def toggle_active(self, request, pk=None):
        ad = self.get_object()
        ad.is_active = not ad.is_active
        ad.save()
        return Response({"is_active": ad.is_active})