import os
from django.core.exceptions import ValidationError

ALLOWED_VIDEO_EXT = [".mp4", ".mov", ".webm", ".mkv",".ts"]
ALLOWED_IMAGE_EXT = [".jpg", ".jpeg", ".png", ".webp"]

MAX_VIDEO_SIZE = 300 * 1024 * 1024
MAX_IMAGE_SIZE = 5 * 1024 * 1024

def validate_video_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_VIDEO_EXT:
        raise ValidationError("Only MP4, MOV, WEBM, and MKV videos are allowed.")
    if file.size > MAX_VIDEO_SIZE:
        raise ValidationError("Video size cannot exceed 300MB.")

def validate_image_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXT:
        raise ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError("Image size cannot exceed 5MB.")
