import jwt
import pytest
from django.conf import settings
from rest_framework import test


@pytest.fixture
def token() -> str:
    token = jwt.encode(
        {"username": "foo", "password": "bar"}, settings.SECRET_KEY
    )
    return token.decode("utf-8")


@pytest.fixture
def api_client(token):
    client = test.APIClient()
    client.credentials(**{"Authorization": "Token " + token})
    return client
