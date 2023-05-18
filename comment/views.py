import logging
from django.core.cache import cache
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentOnPostSerializer, ReplyOnCommentSerializer, CommentSerializer
from paginations.paginations import CustomPagination
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger('comment')


class CommentAPIView(APIView):
    serializer_class = CommentOnPostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CommentOnPostSerializer, operation_id='CreateCommentOnPost')
    def post(self, request):
        """Create new comment on post"""

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info('Comment created on post {}'.format(request.data['post']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetPostComment(ListAPIView):
    """Get post all comments"""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['post_id']

        cache_key = f'post_comments_{post_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info('Comment get from cache: {}'.format(cached_data))
            return cached_data

        queryset = Comment.objects.filter(post_id=post_id).order_by('created')
        cache.set(cache_key, queryset)
        logger.info('Comment set into cache: {}'.format(cached_data))
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_PATH, description='ID of the post', type=openapi.TYPE_INTEGER)
        ],
        operation_id='GetPostComments'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReplyAPIView(APIView):
    serializer_class = ReplyOnCommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ReplyOnCommentSerializer, operation_id='CreateReplyOnPost')
    def post(self, request):
        """Create a reply on the specified comment"""

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("Created reply on the comment: {}".format(request.data['comment_id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)