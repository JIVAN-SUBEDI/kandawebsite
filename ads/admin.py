from django.contrib import admin

# Register your models here.
# ads/admin.py
from django.contrib import admin
from .models import Ad

admin.site.register(Ad)