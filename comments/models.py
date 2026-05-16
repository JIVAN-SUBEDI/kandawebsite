from django.db import models
from videos.models import Video

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=120, blank=True, null=True)
    comment_text = models.TextField()
    ip_address = models.GenericIPAddressField()
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)