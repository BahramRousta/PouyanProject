from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer


class PostAIPView(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        pass

    def post(self, request):
        """Create new post"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request):
        pass