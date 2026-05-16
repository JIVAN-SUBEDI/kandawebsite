from django.db import models

class Ad(models.Model):
    class AdType(models.TextChoices):
        BANNER = "banner", "Banner"
        POPUP = "popup", "Popup"
        VIDEO = "video", "Video"
        SCRIPT = "script", "Script Ad"   # Adsterra script ads

    title = models.CharField(max_length=255)

    ad_type = models.CharField(
        max_length=20,
        choices=AdType.choices
    )

    # Normal ads
    image = models.ImageField(
        upload_to="ads/images/",
        blank=True,
        null=True
    )

    video_file = models.FileField(
        upload_to="ads/videos/",
        blank=True,
        null=True
    )

    target_url = models.URLField(
        blank=True,
        null=True
    )

    # Adsterra / external ad network script
    script_code = models.TextField(
        blank=True,
        null=True,
        help_text="Paste Adsterra ad script here"
    )

    # Controls
    is_active = models.BooleanField(default=True)

    show_on_home = models.BooleanField(default=False)

    show_on_video_details = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.ad_type})"