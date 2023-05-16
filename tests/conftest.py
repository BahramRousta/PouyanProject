import pytest
from django.contrib.auth import get_user_model
from post.models import Post

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
