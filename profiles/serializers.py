"""
Serializers imported for encoded output
"""
from rest_framework import serializers
from followers.models import Follower
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Class for profile serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    following_id = serializers.SerializerMethodField()
    posts_total = serializers.ReadOnlyField()
    followers_total = serializers.ReadOnlyField()
    following_total = serializers.ReadOnlyField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Get request for owner
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        """
        Get following id request
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        """
        Profile model fields
        """
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id', 'posts_total',
            'followers_total', 'following_total'
        ]
