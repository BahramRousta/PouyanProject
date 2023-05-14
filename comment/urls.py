from django.urls import path
from .views import CommentAPIView, ReplyAPIView

urlpatterns = [
    path('comment/', CommentAPIView.as_view(), name='comment'),
    path('reply/', ReplyAPIView.as_view(), name='reply')
]