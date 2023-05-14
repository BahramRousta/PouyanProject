from rest_framework import serializers
from .models import Post
from account.models import Profile


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)


class PostAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['user']


class GetUserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content', 'like', 'comment']
