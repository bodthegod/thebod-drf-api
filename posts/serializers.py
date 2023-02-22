from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Class for post serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.id')

    def validate_image(self, value):
        """
        Validates images by checking file size/height/width
        and displays error if too large
        """
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width is wider than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height is more than 4096px'
            )
        if value.size > 1024 * 1024 * 4:
            raise serializers.ValidationError(
                'Image size is larger than 4MB'
            )
        return value

    def get_is_owner(self, obj):
        """
        returns if user is owner
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        """
        All fields associated with Post model
        """
        model = Post
        fields = ['id', 'owner', 'is_owner', 'profile_id', 'profile_image',
                  'created_at', 'updated_at', 'title', 'content', 'image',
                  'tags', ]
