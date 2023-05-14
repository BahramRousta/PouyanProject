from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/v1/', include('account.urls')),
    path('comment/v1/', include('comment.urls')),
    path('post/v1/', include('post.urls')),
]
