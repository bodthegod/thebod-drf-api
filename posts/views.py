from rest_framework import generics, permissions, filters
from django.db.models import Count
from thebod_drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    Postlist class to display all posts, enable permissions to 
    make users login to make changes
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_total=Count('likes', distinct=True),
        comments_total=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'title',
        'owner__username'
    ]
    ordering_fields = [
        'comments_total',
        'likes_total',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Post Detail class for specific posts (have to be owner)
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_total=Count('likes', distinct=True),
        comments_total=Count('comment', distinct=True)
    ).order_by('-created_at')
