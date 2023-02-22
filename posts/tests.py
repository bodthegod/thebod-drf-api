from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post


class PostListViewTests(APITestCase):
    """
    Tests for postlistview
    """
    def setUp(self):
        User.objects.create_user(username='joe', password='password')

    def test_can_list_posts(self):
        """
        Tests if a user can list any post
        """
        joe = User.objects.get(username='joe')
        Post.objects.create(owner=joe, title='joes title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

