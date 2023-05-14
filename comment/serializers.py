from rest_framework import serializers
from comment.models import Comment, Reply


class CommentPostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['post_id', 'content']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)


class ReplySerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField()

    class Meta:
        model = Reply
        fields = ['comment_id', 'content']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)