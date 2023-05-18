import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestProfile:

    def test_profile_model(self, user):
        """User profile must create automatically when creating a new user"""

        assert User.objects.count() == 1
        assert user.profile is not None

    def test_profile_str_method(self, user):

        assert str(user) == 'testuser'