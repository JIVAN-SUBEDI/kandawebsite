from rest_framework import serializers
from .models import Video, VideoReaction
from .validators import validate_video_file, validate_image_file

class VideoSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Video
        fields = "__all__"
        read_only_fields = [
            "views_count", "likes_count", "dislikes_count",
            "created_by", "created_at", "updated_at"
        ]

    def validate_video_file(self, value):
        validate_video_file(value)
        return value

    def validate_thumbnail(self, value):
        validate_image_file(value)
        return value

    def validate_preview_video(self, value):
        if value:
            validate_video_file(value)
        return value