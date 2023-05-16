from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentOnPostSerializer, ReplyOnCommentSerializer, CommentSerializer
from paginations.paginations import CustomPagination


class CommentAPIView(APIView):
    serializer_class = CommentOnPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Post new comment"""

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetPostComment(ListAPIView):
    """Get post all comments"""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('created')


class ReplyAPIView(APIView):
    serializer_class = ReplyOnCommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a reply on the specified comment"""

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)