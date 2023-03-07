"""
Users within django auth model ↓
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Like
from .models import Post


class LikeListViewTests(APITestCase):
    """
    Tests for likelistview
    """

    def setUp(self):
        User.objects.create_user(username='joe', password='password')

    def test_logged_out_user_cant_like_post(self):
        """
        Tests for if a non authenticated user can like a post (should not)
        """
        response = self.client.post('/likes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    """
    Tests for details of likes (individual likes on posts)
    """

    def setUp(self):
        """
        Creates two user objects containing one post per user
        """
        joe = User.objects.create_user(username='joe', password='joespassword')
        bob = User.objects.create_user(username='bob', password='bobspass')
        Post.objects.create(
            owner=joe, tags='Bodybuilding', title='joes title'
        )
        Post.objects.create(
            owner=bob, tags='Bodybuilding', title='bobs title'
        )
        Like.objects.create(owner=joe, post_id=2)
        Like.objects.create(owner=bob, post_id=1)

    def test_authenticated_user_can_like_posts(self):
        """
        Test to check if an authenticated user can like an existing post
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.post('/likes/', {'post': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cant_get_invalid_like(self):
        """
        Test to see if a user can retrieve an invalid like (like id that hasn't
        been created yet)
        """
        response = self.client.get('/likes/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_get_valid_like(self):
        """
        Test if a user can get a like that is valid (id exists)
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.get('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_remove_own_like(self):
        """
        Test to check if a logged in user can remove their own like
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.delete('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_remove_different_user_like(self):
        """
        Test if a user can delete a like they have not created
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.delete('/likes/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
