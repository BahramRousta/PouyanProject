import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from comment.models import Comment, Reply
from comment.serializers import CommentOnPostSerializer, ReplyOnCommentSerializer, CommentSerializer

User = get_user_model()


@pytest.mark.django_db
class TestCommentAPIView:
    def test_post_comment(self, api_client, user, post):

        api_client.force_authenticate(user=user)

        data = {'post': post.id, 'content': 'Test comment'}

        response = api_client.post('/comment/v1/add_comment/', data)
        assert response.status_code == status.HTTP_201_CREATED

        comment = Comment.objects.get(post=post)
        serializer = CommentOnPostSerializer(comment)
        assert response.data == serializer.data

    def test_post_not_found_comment(self, api_client, user):

        api_client.force_authenticate(user=user)

        data = {'post_id': 1, 'content': 'Test comment'}

        response = api_client.post('/comment/v1/add_comment/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetPostComment:
    def test_get_post_comments(self, api_client, user, post, comment):

        api_client.force_authenticate(user=user)

        response = api_client.get(f'/comment/v1/get_post_comments/{post.id}')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestReplyAPIView:
    def test_create_reply(self, api_client, user, post, comment):
        api_client.force_authenticate(user=user)

        data = {'comment_id': comment.id, 'content': 'Test reply'}
        response = api_client.post('/comment/v1/add_reply/', data)
        assert response.status_code == status.HTTP_201_CREATED

        reply = Reply.objects.get(comment=comment)
        serializer = ReplyOnCommentSerializer(reply)
        assert response.data == serializer.data


