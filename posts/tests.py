"""
Users within django auth model ↓
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post


class PostListViewTests(APITestCase):
    """
    Tests for postlistview (all posts listings)
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
        response = self.client.post('/posts/', {'title': 'new title',
                                                'tags': 'Bodybuilding'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        """
        Tests for if a non authenticated user can create a post (should not)
        """
        response = self.client.post('/posts/', {'title': 'a title',
                                                'tags': 'Running'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_post_without_title(self):
        """
        Test that a post should not be able to be created
        without a title
        """
        self.client.login(username='joe', password='password')
        response = self.client.post('/posts/', {'tags': 'Running'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostDetailViewTests(APITestCase):
    """
    Tests for details of posts (individual posts)
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

    def test_get_created_post(self):
        """
        Test to get a post that has been created by a user (doesn't have to
        be logged in)
        """
        response = self.client.get('/posts/2/')
        self.assertEqual(response.data['title'], 'bobs title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_get_invalid_post(self):
        """
        Test to see if a user can retrieve an invalid post (post id that hasn't
        been created yet)
        """
        response = self.client.get('/posts/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_delete_own_post(self):
        """
        Test to check if a logged in user can delete their own post
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.delete('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_remove_different_user_post(self):
        """
        Test if a user can delete a post they have not created
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.delete('/posts/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_edit_own_post(self):
        """
        Test if a user can edit a post they created
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.put(
            '/posts/1/', {'title': 'joes edited title!', 'tags': 'Running'})
        new_post = Post.objects.filter(pk=1).first()
        self.assertEqual(new_post.title, 'joes edited title!')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_edit_other_post(self):
        """
        Test if a user can edit a post they did not create or own
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.put(
            '/posts/2/', {'title': 'joes edited title!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
