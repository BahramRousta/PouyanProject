import pytest
from comment.models import Comment


@pytest.mark.django_db
class TestComment:

    def test_comment_model(self, comment):

        assert Comment.objects.count() == 1

    def test_comment_str_representation(self, user, post, comment):
        expected_str = f'Comment by {user.username} on {post}'

        assert str(comment) == expected_str

    def test_comment_ordering(self, user, post):
        comment1 = Comment.objects.create(author=user.profile, post=post, content='Comment 1')
        comment2 = Comment.objects.create(author=user.profile, post=post, content='Comment 2')

        comments = Comment.objects.filter(post=post).order_by('-created')

        assert comments[0] == comment2
        assert comments[1] == comment1