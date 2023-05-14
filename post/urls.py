from django.urls import path
from .views import PostAIPView
urlpatterns = [
    path('create_post/', PostAIPView.as_view(), name='create-post'),
]