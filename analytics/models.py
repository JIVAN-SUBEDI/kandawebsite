from django.conf import settings
from django.db import models
from videos.models import Video
from ads.models import Ad

class ActivityLog(models.Model):
    class Action(models.TextChoices):
        VIEW = "view", "View"
        LIKE = "like", "Like"
        DISLIKE = "dislike", "Dislike"
        COMMENT = "comment", "Comment"
        AD_IMPRESSION = "ad_impression", "Ad Impression"
        AD_CLICK = "ad_click", "Ad Click"
        UPLOAD = "upload", "Upload"

    action = models.CharField(max_length=50, choices=Action.choices)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)
    ad = models.ForeignKey(Ad, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)