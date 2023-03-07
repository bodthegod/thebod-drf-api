"""
Django config for the app ↓
"""
from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """
    Configuration for comments within django
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
