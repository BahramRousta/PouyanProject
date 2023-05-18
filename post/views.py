import logging
from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Profile
from account.serializers import ProfileSerializer
from .models import Post
from .serializers import PostSerializer, GetUserPostSerializer
from paginations.paginations import CustomPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


logger = logging.getLogger('post')


class PostAIPView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_PATH, description='username of user', type=openapi.TYPE_STRING)
        ],
        operation_id='GetPostsByUsername'
    )
    def get(self, request, username):
        """Receive username and return user's all posts"""

        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            logger.info('User {} not found'.format(username))
            return Response(
                data={"Message": f"User {username} dose not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the data is already cached
        cache_key = f'user_posts_{username}'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info('User post get from cache: {}'.format(cache_key))
            return Response(cached_data, status=status.HTTP_200_OK)

        posts = Post.objects.filter(author__user__username=username)

        if len(posts) == 0:
            return Response(
                data={"Message": f"User {username} do not have any post yet."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GetUserPostSerializer(posts, many=True)
        data = serializer.data

        # Cache the data for future requests
        cache.set(cache_key, data)
        logger.info('User post set into cache'.format(cache_key))
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PostSerializer, operation_id='CreatePost')
    def post(self, request):
        """Create new post"""

        serializer = PostSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info('Post created')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_PATH, description='ID of post', type=openapi.TYPE_INTEGER)
        ],
        operation_id='LikeUserPost'
    )
    def patch(self, request, post_id, format=None):
        """Like users' posts"""

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            logger.info('Post not found')
            return Response(
                {'message': 'Post does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get user profile
        user = request.user.profile

        if post.like.filter(id=user.id).exists():
            return Response(
                {'message': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.like.add(user)

        return Response(
            data={'Message': 'Post liked successfully.'},
            status=status.HTTP_201_CREATED
        )


class PostsLikesAPIVIew(ListAPIView):
    """Returns a list of users who have liked posts"""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['post_id']

        # Check if the data is already cached
        cache_key = f'post_likes_{post_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info('Post likes get from cache'.format(cache_key))
            return cached_data

        queryset = Profile.objects.filter(
            pk__in=Post.objects.filter(pk=post_id)
            .prefetch_related(
                Prefetch('like', queryset=Profile.objects.select_related('user'))
            )
            .values_list('like__pk', flat=True)
        )

        # Cache the queryset for future requests
        cache.set(cache_key, queryset)
        logger.info('Liked post set into cache'.format(cache_key))
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_PATH, description='ID of post', type=openapi.TYPE_INTEGER)
        ],
        operation_id='GetUserWhoLikePost'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)