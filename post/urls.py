from django.urls import path
from .views import PostAIPView, LikePostAPIView, PostsLikesAPIVIew
urlpatterns = [
    path('create_post/', PostAIPView.as_view(), name='create-post'),
    path('get_posts/<str:username>', PostAIPView.as_view(), name='get-posts'),
    path('like_post/<int:post_id>', LikePostAPIView.as_view(), name='like-post'),
    path('users_liked_post/<int:post_id>', PostsLikesAPIVIew.as_view(), name='users-liked-post'),
]