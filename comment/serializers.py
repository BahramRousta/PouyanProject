from rest_framework import serializers
from account.serializers import ProfileSerializer
from comment.models import Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Reply
        fields = ('author', 'content')


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)
    author = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ('author', 'content', 'replies')


class CommentOnPostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'content']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)


class ReplyOnCommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField()

    class Meta:
        model = Reply
        fields = ['id', 'comment_id', 'content']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)