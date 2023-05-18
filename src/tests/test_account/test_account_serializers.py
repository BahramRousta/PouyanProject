import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from account.serializers import UserSerializer, LoginSerializer, ObtainTokenSerializer, ProfileSerializer

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializer:
    def test_user_serializer_valid_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'password2': 'testpass',
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()

        user = serializer.save()
        assert isinstance(user, User)
        assert user.username == 'testuser'
        assert user.check_password('testpass')

    def test_user_serializer_invalid_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'password2': 'differentpass',
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestLoginSerializer:
    def test_login_serializer_fields(self):
        serializer = LoginSerializer()
        assert 'username' in serializer.fields
        assert 'password' in serializer.fields

    def test_login_serializer_valid_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid()

    def test_login_serializer_invalid_data(self):
        data = {
            'username': 'testuser',
            'password': ''
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()


class TestObtainTokenSerializer:
    def test_obtain_token_serializer_fields(self):
        serializer = ObtainTokenSerializer()
        assert 'access_token' in serializer.fields
        assert 'access_token_expiration' in serializer.fields
        assert 'refresh_token' in serializer.fields
        assert 'refresh_token_expiration' in serializer.fields


@pytest.mark.django_db
class TestProfileSerializer:
    def test_profile_serializer_username(self):
        user = User.objects.create_user(username='testuser', password='testpass')

        serializer = ProfileSerializer(instance=user.profile)
        assert serializer.data['username'] == 'testuser'

