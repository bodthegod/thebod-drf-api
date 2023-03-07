from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profile


class ProfileDetailViewTests(APITestCase):
    """
    Tests for specific user methods tied to a profile
    """
    def setUp(self):
        """
        Creates two user objects for the setup
        """
        User.objects.create_user(username='joe', password='joespassword')
        User.objects.create_user(username='bob', password='bobspass')

    def test_user_can_edit_self_profile(self):
        """
        Test if possible for a user to edit their profile
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.put('/profiles/1/', {'content': 'i can edit! :)'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.content, 'i can edit! :)')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_edit_other_profiles(self):
        """
        Test if a user can't edit other profiles that they do not own
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.put('/profiles/2/', {'content': 'i cant edit :('})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_view_profiles(self):
        """
        Test if possible for a user to view a profile by its ID
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_view_null_profile(self):
        """
        Test if a null profile (no /id) is viewable
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.get('/profiles/200/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cant_edit_profile(self):
        """
        Test if an unauthenticated user can't edit a profile
        """
        response = self.client.put('/profiles/2/', {'content': 'i still cant edit :('})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

