from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Comment

User = get_user_model()


# Hyperlink view Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'title',
        )


# Hyperlink view Serializer
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class PostSerializer(serializers.ModelSerializer):
    # Hyperlink identity
    owner = serializers.HyperlinkedIdentityField(many=False, view_name='owner-view', )
    # Hyperlink Related Field
    comments = serializers.HyperlinkedRelatedField(queryset=Comment.objects.all(), many=True, view_name='comment-view', )

    class Meta:
        model = Post
        fields = (
            'title',
            'owner',
            'custom_id',
            'category',
            'publish_date',
            'last_updated',
            'comments',
        )
