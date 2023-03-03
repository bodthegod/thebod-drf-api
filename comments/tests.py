from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from .models import Comment


class CommentListViewTests(APITestCase):
    def setUp(self):
        """
        Automatically runs before every test method
        """
        User.objects.create_user(username='joe', password='joespass')

    def test_logged_out_user_cannot_create_comment(self):
        """
        Test to make sure if logged out commenting is forbidden
        """
        response = self.client.post(
            '/comments/', {'comment_info': 'joes comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        """
        Creates two user objects containing one commment and one post each
        """
        joe = User.objects.create_user(username='joe', password='joespassword')
        bob = User.objects.create_user(username='bob', password='bobspass')
        Post.objects.create(
            owner=joe, title='joes title'
        )
        Post.objects.create(
            owner=bob, title='bobs title'
        )
        Comment.objects.create(owner=joe, post_id=1,
                               comment_info='joes first comment')
        Comment.objects.create(owner=bob, post_id=2,
                               comment_info='bobs first comment')

    def test_logged_in_user_can_create_comment(self):
        """
        Test if possible for a logged in user to create a comment
        """
        self.client.login(username='joe', password='joespassword')
        response = self.client.post('/comments/', {'post': 1,
                                                   'comment_info': 'second comment'})
        comment_total = Comment.objects.count()
        self.assertEqual(comment_total, 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_created_comment(self):
        """
        Test to get a previously created comment by pk
        """
        self.client.login(username='joe', password='password')
        response = self.client.get('/comments/1/')
        self.assertEqual(response.data['comment_info'], 'joes first comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
