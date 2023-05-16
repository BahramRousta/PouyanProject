import pytest
from django.contrib.auth import get_user_model
from comment.models import Comment
from post.models import Post
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass'
    )


@pytest.fixture
def post(user):
    return Post.objects.create(
        content="posttest",
        author=user.profile
    )


@pytest.fixture
def comment(user, post):
    return Comment.objects.create(
        author=user.profile,
        post=post,
        content="commenttes",
    )


@pytest.fixture
def api_client():
    return APIClient()