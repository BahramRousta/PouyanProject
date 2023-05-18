import pytest
from django.contrib.auth import get_user_model
from account.serializers import ProfileSerializer
from comment.models import Comment, Reply
from comment.serializers import CommentSerializer, CommentOnPostSerializer, ReplyOnCommentSerializer

User = get_user_model()


@pytest.mark.django_db
class TestCommentSerializer:
    def test_comment_serializer_replies(self, user, post):
        comment = Comment.objects.create(author=user.profile, content='Test comment', post=post)
        Reply.objects.create(author=user.profile, content='Test reply', comment=comment)

        serializer = CommentSerializer(instance=comment)
        assert len(serializer.data['replies']) == 1
        assert serializer.data['replies'][0]['author'] == ProfileSerializer(instance=user.profile).data
        assert serializer.data['replies'][0]['content'] == 'Test reply'


@pytest.mark.django_db
class TestCommentOnPostSerializer:
    def test_comment_on_post_serializer_valid_data(self, user, post, rf):

        request = rf.post('/comment/v1/add_comment/')
        request.user = user

        data = {
            'post': post.id,
            'content': 'Test comment',
        }
        serializer = CommentOnPostSerializer(data=data, context={'request': request})
        assert serializer.is_valid()

        comment = serializer.save()
        assert isinstance(comment, Comment)
        assert comment.content == 'Test comment'
        assert comment.author == user.profile


@pytest.mark.django_db
class TestReplyOnCommentSerializer:
    def test_reply_on_comment_serializer_valid_data(self, user, comment, rf):

        request = rf.post('/comment/v1/add_reply/')
        request.user = user

        data = {
            'comment_id': comment.id,
            'content': 'Test reply',
        }
        serializer = ReplyOnCommentSerializer(data=data, context={'request': request})
        assert serializer.is_valid()

        reply = serializer.save()
        assert isinstance(reply, Reply)
        assert reply.content == 'Test reply'
        assert reply.author == user.profile

