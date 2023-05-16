import pytest
from post.models import Post


@pytest.mark.django_db
class TestPostModel:

    def test_post_model(self, post, user):
        """Test creating a post"""

        assert Post.objects.count() == 1
        assert post.content == "posttest"
        assert post.like.count() == 0
        assert post.author == user.profile

    def test_post_str_method(self, post):
        """Test post string method"""

        assert str(post) == "Post posttest by testuser"

    def test_post_like(self, post, user):
        """Test post like count"""

        post.like.add(user.profile)

        assert post.like.count() == 1
        assert user.profile in post.like.all()