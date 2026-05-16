from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import IsAdminOrStaffRole
from analytics.models import ActivityLog
from videos.models import Video
from comments.models import Comment

User = get_user_model()

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdminOrStaffRole]

    def get(self, request):
        period = request.query_params.get("period", "today")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        now = timezone.now()

        if period == "today":
            start_date = now.replace(hour=0, minute=0, second=0)
        elif period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "year":
            start_date = now - timedelta(days=365)
        elif period == "custom" and start and end:
            start_date = start
        else:
            start_date = now.replace(hour=0, minute=0, second=0)

        logs = ActivityLog.objects.filter(created_at__gte=start_date)

        daily = (
            logs.annotate(date=TruncDate("created_at"))
            .values("date", "action")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        recent = logs.order_by("-created_at")[:10].values(
            "id", "action", "created_at", "video__title", "ad__title"
        )

        return Response({
            "total_videos": Video.objects.count(),
            "total_views": logs.filter(action="view").count(),
            "total_likes": logs.filter(action="like").count(),
            "total_dislikes": logs.filter(action="dislike").count(),
            "total_comments": Comment.objects.count(),
            "total_users": User.objects.count(),
            "recent_activity": list(recent),
            "daily_analytics": list(daily),
        })