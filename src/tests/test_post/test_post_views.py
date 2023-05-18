import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from post.models import Post
from post.serializers import PostSerializer, GetUserPostSerializer

User = get_user_model()


@pytest.mark.django_db
class TestPostAIPView:
    def test_get_user_posts(self, api_client, user, post):

        api_client.force_authenticate(user=user)

        response = api_client.get(f'/post/v1/get_posts/{user.username}')
        assert response.status_code == status.HTTP_200_OK

        serializer = GetUserPostSerializer([post], many=True)
        assert response.data == serializer.data

    def test_get_user_posts_user_not_found(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get('/post/v1/get_posts/none')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'Message': 'User none dose not exist'}

    def test_get_user_posts_no_posts(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/post/v1/get_posts/{user.username}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'Message': f'User {user.username} do not have any post yet.'}

    def test_create_post(self, api_client, user):

        api_client.force_authenticate(user=user)

        data = {'content': 'Test post'}
        response = api_client.post('/post/v1/create_post/', data)
        assert response.status_code == status.HTTP_201_CREATED

        post = Post.objects.get(author=user.profile)
        serializer = PostSerializer(post)
        assert response.data == serializer.data


@pytest.mark.django_db
class TestLikePostAPIView:
    def test_like_post(self, api_client, user, post):

        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/post/v1/like_post/{post.id}')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'Message': 'Post liked successfully.'}

        post.refresh_from_db()
        assert post.like.count() == 1
        assert user.profile in post.like.all()

    def test_like_post_post_not_found(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.patch('/post/v1/like_post/123')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_like_post_already_liked(self, api_client, user, post):

        post.like.add(user.profile)

        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/post/v1/like_post/{post.id}')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'message': 'You have already liked this post.'}
