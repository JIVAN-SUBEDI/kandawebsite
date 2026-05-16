# videos/admin.py
from django.contrib import admin
from .models import Video, VideoReaction

admin.site.register(Video)
admin.site.register(VideoReaction)