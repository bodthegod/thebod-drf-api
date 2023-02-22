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

    def test_logged_in_user_can_create_post(self):
        """
        Tests if a logged in user can create a post
        """
        self.client.login(username='joe', password='password')
        response = self.client.post('/posts/', {'title': 'new title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        """
        Tests for if a non authenticated user can create a post (should not)
        """
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
