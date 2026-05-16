from django.db.models import F
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts.permissions import IsAdminOrStaffRole
from analytics.models import ActivityLog
from .models import Video, VideoReaction
from .serializers import VideoSerializer
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.db.models import F

import mimetypes


def get_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0]
    return request.META.get("REMOTE_ADDR")



class PublicVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]
    @action(detail=True, methods=["get"], url_path="stream")
    def stream(self, request, pk=None):
        video = self.get_object()

        referer = request.META.get("HTTP_REFERER", "")
        origin = request.META.get("HTTP_ORIGIN", "")

        allowed_domains = [
            "http://localhost:3000",
            "http://localhost:8000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://your-frontend-domain.com",
        ]

        allowed = any(domain in referer for domain in allowed_domains) or any(
            domain in origin for domain in allowed_domains
        )

        if not allowed:
            return HttpResponseForbidden("Direct video access blocked")

        if not video.video_file:
            raise Http404("Video file not found")

        file_path = video.video_file.path
        content_type, _ = mimetypes.guess_type(file_path)

        response = FileResponse(
            open(file_path, "rb"),
            content_type=content_type or "video/mp4",
        )
        response["Content-Disposition"] = "inline"
        response["X-Content-Type-Options"] = "nosniff"
        return response

    @action(detail=True, methods=["post"])
    def view(self, request, pk=None):
        video = self.get_object()

        Video.objects.filter(id=video.id).update(
            views_count=F("views_count") + 1
        )

        ActivityLog.objects.create(
            action=ActivityLog.Action.VIEW,
            video=video,
            ip_address=get_ip(request),
        )

        video.refresh_from_db(fields=["views_count"])

        return Response({
            "message": "View counted.",
            "views_count": video.views_count,
        })

    @action(detail=True, methods=["post"])
    def react(self, request, pk=None):
        video = self.get_object()
        reaction_type = request.data.get("reaction")
        fingerprint = request.data.get("fingerprint", "")

        if reaction_type not in ["like", "dislike"]:
            return Response(
                {"error": "Reaction must be like or dislike."},
                status=400,
            )

        ip = get_ip(request)

        reaction, created = VideoReaction.objects.get_or_create(
            video=video,
            ip_address=ip,
            fingerprint=fingerprint,
            defaults={"reaction": reaction_type},
        )

        if not created and reaction.reaction == reaction_type:
            video.refresh_from_db(fields=["likes_count", "dislikes_count"])

            return Response({
                "message": "Already reacted.",
                "likes_count": video.likes_count,
                "dislikes_count": video.dislikes_count,
            })

        if created:
            if reaction_type == "like":
                Video.objects.filter(id=video.id).update(
                    likes_count=F("likes_count") + 1
                )
            else:
                Video.objects.filter(id=video.id).update(
                    dislikes_count=F("dislikes_count") + 1
                )
        else:
            if reaction.reaction == "like" and reaction_type == "dislike":
                Video.objects.filter(id=video.id).update(
                    likes_count=F("likes_count") - 1,
                    dislikes_count=F("dislikes_count") + 1,
                )

            elif reaction.reaction == "dislike" and reaction_type == "like":
                Video.objects.filter(id=video.id).update(
                    dislikes_count=F("dislikes_count") - 1,
                    likes_count=F("likes_count") + 1,
                )

            reaction.reaction = reaction_type
            reaction.save(update_fields=["reaction"])

        ActivityLog.objects.create(
            action=reaction_type,
            video=video,
            ip_address=ip,
        )

        video.refresh_from_db(fields=["likes_count", "dislikes_count"])

        return Response({
            "message": f"{reaction_type} saved.",
            "likes_count": video.likes_count,
            "dislikes_count": video.dislikes_count,
        })

class AdminVideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("-created_at")
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrStaffRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        video = serializer.save(created_by=self.request.user)
        ActivityLog.objects.create(
            action=ActivityLog.Action.UPLOAD,
            video=video,
            user=self.request.user
        )

    @action(detail=True, methods=["post"])
    def toggle_active(self, request, pk=None):
        video = self.get_object()
        video.is_active = not video.is_active
        video.save()
        return Response({"is_active": video.is_active})