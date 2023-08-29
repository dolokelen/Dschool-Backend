import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate_superuser(api_client):
    def do_authenticate_superuser(is_superuser=False):
        return api_client.force_authenticate(user=User(is_superuser=is_superuser))
    return do_authenticate_superuser

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate


