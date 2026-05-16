from rest_framework import serializers
from .models import Comment

BLOCKED_WORDS = ["spam", "fake", "casino", "adult"]
BLOCKED_LINKS = ["http://", "https://", "www."]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "video", "name", "comment_text", "is_approved", "created_at"]
        read_only_fields = ["is_approved", "created_at"]

    def validate_comment_text(self, value):
        text = value.strip()

        if not text:
            raise serializers.ValidationError("Comment cannot be empty.")

        if len(text) > 500:
            raise serializers.ValidationError("Comment cannot exceed 500 characters.")

        lower_text = text.lower()

        if any(word in lower_text for word in BLOCKED_WORDS):
            raise serializers.ValidationError("Suspicious words are not allowed.")

        if any(link in lower_text for link in BLOCKED_LINKS):
            raise serializers.ValidationError("Links are not allowed in comments.")

        return text