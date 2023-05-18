from rest_framework import serializers
from comment.serializers import CommentSerializer
from .models import Post
from account.models import Profile


class PostSerializer(serializers.ModelSerializer):
    """Serializer for creating posts."""

    class Meta:
        model = Post
        fields = ['id', 'content']

    def create(self, validated_data):

        # Set post author
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)


class PostAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['user']


class GetUserPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = serializers.SerializerMethodField()

    def get_likes(self, post):
        return post.like.count()

    class Meta:
        model = Post
        fields = ('id', 'content', 'likes', 'comments')


