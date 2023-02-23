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
