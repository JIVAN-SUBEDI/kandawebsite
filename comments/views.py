from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.permissions import IsAdminOrStaffRole
from analytics.models import ActivityLog
from .models import Comment
from .serializers import CommentSerializer

def get_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0]
    return request.META.get("REMOTE_ADDR")

class PublicCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        video_id = self.request.query_params.get("video")
        qs = Comment.objects.filter(is_approved=True, is_spam=False).order_by("-created_at")
        if video_id:
            qs = qs.filter(video_id=video_id)
        return qs

    def perform_create(self, serializer):
        ip = get_ip(self.request)
        recent_count = Comment.objects.filter(
            ip_address=ip,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).count()

        is_spam = recent_count >= 3

        comment = serializer.save(
            ip_address=ip,
            is_spam=is_spam,
            is_approved=True
        )

        ActivityLog.objects.create(
            action=ActivityLog.Action.COMMENT,
            video=comment.video,
            ip_address=ip
        )

class AdminCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrStaffRole]

    def partial_update(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.is_approved = request.data.get("is_approved", comment.is_approved)
        comment.is_spam = request.data.get("is_spam", comment.is_spam)
        comment.save()
        return Response(CommentSerializer(comment).data)