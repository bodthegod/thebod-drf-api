from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Follower


class FollowerListViewTests(APITestCase):
    """
    Tests for followerlistview
    """

    def setUp(self):
        User.objects.create_user(username='joe', password='password')

    def test_unauth_prevent_follow(self):
        """
        Tests if an unauthenticated user cant follow
        """
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
