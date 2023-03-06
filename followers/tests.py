from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Follower


class FollowerListViewTests(APITestCase):
    """
    Tests for followerlistview
    """

    def setUp(self):
        """
        Setup for followerlistviewtests with one user object
        """
        User.objects.create_user(username='joe', password='joes password')

    def test_unauth_prevent_follow(self):
        """
        Tests if an unauthenticated user cant follow
        """
        response = self.client.post('/followers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FollowerDetailViewTests(APITestCase):
    """
    Tests for followerdetailviewtests with multiple user objects
    """

    def setUp(self):
        """
        Setup to create 3 user objects and assign each to followed
        """
        joe = User.objects.create_user(
            username='joe', password='joes password')
        bob = User.objects.create_user(
            username='bob', password='bobs password')
        sam = User.objects.create_user(
            username='sam', password='sams password')

        Follower.objects.create(owner=joe, followed_id=1)
        Follower.objects.create(owner=bob, followed_id=2)
        Follower.objects.create(owner=sam, followed_id=3)

    def test_user_can_view_following_using_valid_id(self):
        """
        Test to allow user to view a users following
        using followers/<int:pk>/
        """
        self.client.login(username='joe', password='joes password')
        response = self.client.get('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_follow_profiles(self):
        """
        Test to check if an authenticated user can follow
        any created profile
        """
        self.client.login(username='joe', password='joes password')
        response = self.client.post('/followers/', {'followed': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unfollow_other_user_following(self):
        """
        Test to check if a user can unfollow a different
        profiles following using followers/<int:pk>/
        """
        self.client.login(username='joe', password='joes password')
        response = self.client.delete('/followers/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_unfollow_profiles(self):
        """
        Test to check if a user can unfollow a profile
        they currently follow using followers/<int:pk>/
        """
        self.client.login(username='joe', password='joes password')
        response = self.client.delete('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_view_following_using_invalid_id(self):
        """
        Test to check if a user can view a following
        that has an invalid id using followers/<int:pk>/
        (has not been created yet)
        """
        self.client.login(username='joe', password='joes password')
        response = self.client.get('/followers/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
