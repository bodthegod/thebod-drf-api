"""
IntegrityError imported from django ↓
"""
from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializes data for likes
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """
        Fields associated with likes
        """
        model = Like
        fields = ['id', 'owner', 'post', 'created_at']

    def create(self, validated_data):
        """
        Error handling for duplicated like result
        from single user
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'duplicated like, error'
            })
