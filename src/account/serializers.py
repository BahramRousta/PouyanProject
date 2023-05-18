from rest_framework import serializers
from core.settings.base import SIMPLE_JWT
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def save(self):
        user = User(
            username=self.validated_data['username']
        )
        password = self.validated_data['password']

        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login request"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )


class ObtainTokenSerializer(serializers.Serializer):
    """Serializer for user authentication"""

    access_token = serializers.CharField(max_length=255)
    access_token_expiration = serializers.CharField(
        default=f"{SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds} seconds"
    )
    refresh_token = serializers.CharField(max_length=255)
    refresh_token_expiration = serializers.CharField(
        default=f"{SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()} seconds"
    )


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username']

    def get_username(self, obj):
        return obj.user.username