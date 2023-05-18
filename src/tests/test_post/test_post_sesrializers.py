import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from account.models import Profile
from post.models import Post
from post.serializers import PostSerializer, PostAuthorSerializer, GetUserPostSerializer

User = get_user_model()


@pytest.mark.django_db
class TestPostSerializer:
    def test_post_serializer_valid_data(self, user, rf):

        request = rf.post('/post/v1/create_post/')
        request.user = user

        data = {
            'content': 'Test content',
        }
        serializer = PostSerializer(data=data, context={'request': request})
        assert serializer.is_valid()

        post = serializer.save()
        assert isinstance(post, Post)
        assert post.content == 'Test content'
        assert post.author == user.profile

    def test_post_serializer_invalid_data(self, user, rf):

        request = rf.post('/post/v1/create_post/')
        request.user = user

        data = {
            'content': '',
        }
        serializer = PostSerializer(data=data, context={'request': request})
        assert not serializer.is_valid()
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestPostAuthorSerializer:
    def test_post_author_serializer_fields(self):
        serializer = PostAuthorSerializer()
        assert 'user' in serializer.fields


@pytest.mark.django_db
class TestGetUserPostSerializer:
    def test_get_user_post_serializer_fields(self):
        serializer = GetUserPostSerializer()
        assert 'id' in serializer.fields
        assert 'content' in serializer.fields
        assert 'likes' in serializer.fields
        assert 'comments' in serializer.fields

    def test_get_user_post_serializer_likes(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        post = Post.objects.create(content='Test content', author=user.profile)
        post.like.add(user.profile)

        serializer = GetUserPostSerializer(instance=post)
        assert serializer.data['likes'] == 1
