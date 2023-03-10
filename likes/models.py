"""
Models imported from django.db ↓
"""
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Like(models.Model):
    """
    Class for the like model, owner as a foreign key, linked to all posts
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        ordered by time created at descending,
        owner and post is unique and keeps
        likes validated
        """
        ordering = ['-created_at']
        unique_together = ['owner', 'post']

    def __str__(self):
        return f'{self.owner} {self.post}'
