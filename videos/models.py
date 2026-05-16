from django.conf import settings
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/")
    preview_video = models.FileField(upload_to="previews/", blank=True, null=True)

    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class VideoReaction(models.Model):
    class Reaction(models.TextChoices):
        LIKE = "like", "Like"
        DISLIKE = "dislike", "Dislike"

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="reactions")
    ip_address = models.GenericIPAddressField()
    fingerprint = models.CharField(max_length=255, blank=True, null=True)
    reaction = models.CharField(max_length=10, choices=Reaction.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("video", "ip_address", "fingerprint")