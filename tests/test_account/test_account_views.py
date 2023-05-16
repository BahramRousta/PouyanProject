import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestRegisterView:
    def test_register_successful(self, api_client):
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'password2': 'testpass',
        }
        response = api_client.post('/account/v1/register/', data)
        assert response.status_code == status.HTTP_200_OK

        user = User.objects.get(username='testuser')
        assert user is not None
        assert user.check_password('testpass')

        token_data = response.json()
        assert 'refresh_token' in token_data
        assert 'access_token' in token_data

    def test_fail_register(self, api_client):
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'password2': 'invalid_password',
        }
        response = api_client.post('/account/v1/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b"Passwords do not match." in response.content


@pytest.mark.django_db
class TestLoginAPIView:
    def test_login_api_view_valid_credentials(self, user, api_client):

        data = {
            'username': 'testuser',
            'password': 'testpass',
        }
        response = api_client.post('/account/v1/login/', data)
        assert response.status_code == status.HTTP_200_OK

        token_data = response.json()
        assert 'refresh_token' in token_data
        assert 'access_token' in token_data

    def test_login_api_view_invalid_credentials(self, api_client):
        data = {
            'username': 'testuser',
            'password': 'testpass',
        }
        response = api_client.post('/account/v1/login/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        error_data = response.json()
        assert 'Message' in error_data
        assert error_data['Message'] == 'The user information is invalid.'
