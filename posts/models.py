from django.db import models
from django.contrib.auth.models import User

class Tags(models.Model):
    """
    Model for tags associated to posts
    """
    tags = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.tags}'


class Post(models.Model):
    """
    Post Model
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_f3qkbi', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'