"""
IntegrityError imported from django ↓
"""
from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializes data for followers
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_username = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        """
        Fields associated with follower
        """
        model = Follower
        fields = ['id', 'owner', 'created_at', 'followed_username', 'followed']

    def create(self, validated_data):
        """
        Error handling for duplicated follow result (only one follow per user)
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'duplicated follow, one follow per user'})
