import logging
from django.contrib.auth import login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import LoginSerializer, ObtainTokenSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema


logger = logging.getLogger('account')


class AuthAPIView(APIView):
    def _obtain_token(self, request, user):
        """Return access and refresh token for user."""

        try:
            refresh = RefreshToken.for_user(user)
            token = ObtainTokenSerializer({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            }).data
            logger.info('Token created: {}'.format(user.username))
            return token
        except Exception as e:
            logger.info('Failed to created token: {}'.format(str(e)))
            raise e


class RegisterView(AuthAPIView):
    """Register API View."""

    permission_classes = [AllowAny]
    serializer_classes = UserSerializer

    @swagger_auto_schema(request_body=UserSerializer, operation_id='RegisterUser')
    def post(self, request):
        serializer = self.serializer_classes(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info('Registered user: {}'.format(user))
            login(request, user)
            logger.info('User {} logged in'.format(user.username))
            return Response(data=self._obtain_token(request, user), status=status.HTTP_200_OK)
        else:
            logger.info('Registration failed: {}'.format(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(AuthAPIView):
    """Login API View. Receive username and password. Return access and refresh token."""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, operation_id='LoginUser')
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Get user from DB
            user = User.objects.filter(username=data["username"]).first()

            # Validate password
            if user and user.check_password(data["password"]):
                login(request, user)
                logger.info('User {} login successful.'.format(user.username))
                return Response(
                    status=status.HTTP_200_OK,
                    data=self._obtain_token(request, user)
                )
            else:
                logger.info('User {} login failed.'.format(user.username))
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={"Message": "The user information is invalid."}
                )
        else:
            logger.info('Login failed: {}'.format(serializer.errors))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
