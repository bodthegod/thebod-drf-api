"""
Models imported from django.db ↓
"""
from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    Class for the follower model, owner as a foreign key, linked to all posts
    functions of following and followed
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        ordered by time created at descending,
        owner and followed is unique and keeps
        follows validated
        """
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} {self.followed}'
