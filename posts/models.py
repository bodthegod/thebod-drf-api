from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post Model
    """
    # tags_array = [
    #     ('Bodybuilding', 'BodyBuilding'),
    #     ('Running', 'Running'),
    #     ('Sports', 'Sports'),
    #     ('Fitness', 'Fitness'),
    #     ('Wellbeing', 'Wellbeing'),
    #     ('Bodybuilding', 'BodyBuilding'),
    # ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    # tags = models.CharField(max_length=20, choices=tags_array)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_f3qkbi', blank=True
    )

    class Meta:
        """
        Orders by time created at
        """
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
