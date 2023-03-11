"""
App Configuration imported from django ↓
"""
from django.apps import AppConfig


class LikesConfig(AppConfig):
    """
    Likes auto field and name configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'likes'
