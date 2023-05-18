import pytest
from comment.models import Comment


@pytest.mark.django_db
class TestCommentModel:

    def test_comment_model(self, comment):

        assert Comment.objects.count() == 1

    def test_comment_str_representation(self, user, post, comment):
        expected_str = f'Comment by {user.username} on {post}'

        assert str(comment) == expected_str
