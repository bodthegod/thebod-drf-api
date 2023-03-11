"""
App Configuration imported from django ↓
"""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """
    Posts auto field and name app configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
