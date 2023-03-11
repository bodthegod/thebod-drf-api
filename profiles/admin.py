"""
Admin module imported from django.contrib ↓
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
