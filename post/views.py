from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Profile
from .models import Post
from .serializers import PostSerializer, GetUserPostSerializer


class PostAIPView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, username):

        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response(data={"Message": f"User {username} dose not exist"})

        posts = Post.objects.filter(author__user__username=username)

        if len(posts) == 0:
            return Response(data={"Message": f"User {username} do not have any post yet."})

        serializer = GetUserPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new post"""

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
