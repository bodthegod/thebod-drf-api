from django.db.models import Count
from rest_framework import generics, filters
from thebod_drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles, annotate to add extra fields to
    queryset
    """
    queryset = Profile.objects.annotate(
        followers_total=Count('owner__followed', distinct=True),
        following_total=Count('owner__following', distinct=True),
        posts_totalt=Count('owner__post', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_total',
        'owner__following__created_at',
        'owner__followed__created_at',
        'followers_total',
        'following_total',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Display details of specific profile based on primary key (has to be owner)
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        followers_total=Count('owner__followed', distinct=True),
        following_total=Count('owner__following', distinct=True),
        posts_total=Count('owner__post', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
