from django.urls import path
from .views import CommentAPIView, ReplyAPIView, GetPostComment

urlpatterns = [
    path('add_comment/', CommentAPIView.as_view(), name='add-comment'),
    path('add_reply/', ReplyAPIView.as_view(), name='add-reply'),
    path('get_post_comments/<int:post_id>', GetPostComment.as_view(), name='get_post_comments')
]