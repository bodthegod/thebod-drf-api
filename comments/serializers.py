from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Class for comment serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Get request for owner of comment
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        """
        Gets created at time in naturaltime format
        """
        return naturaltime(obj.created_at)
    

    def get_updated_at(self, obj):
        """
        Gets updated at time in naturaltime format
        """
        return naturaltime(obj.updated_at)

    class Meta:
        """
        Comment model fields
        """
        model = Comment
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'profile_id',
            'profile_image', 'is_owner', 'post', 'comment_info',
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Class for details of specific comment
    """
    post = serializers.ReadOnlyField(source='post.id')
