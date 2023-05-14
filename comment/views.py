from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CommentPostSerializer, ReplySerializer


class CommentAPIView(APIView):
    serializer_class = CommentPostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReplyAPIView(APIView):
    serializer_class = ReplySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)