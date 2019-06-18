from datetime import datetime, timedelta

import jwt
import pytest
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from v1.authentication import JWTAuthentication


class MockedRequest:
    def __init__(self):
        self.META = {}


@pytest.fixture
def mocked_request_factory():
    def factory(expired=False):
        user_data = {"username": "foo", "password": "bar"}

        if expired:
            user_data["exp"] = datetime.utcnow() - timedelta(hours=1)

        token = jwt.encode(user_data, settings.SECRET_KEY)
        mocked_request = MockedRequest()
        mocked_request.META = {
            "HTTP_AUTHORIZATION": "Token " + token.decode("utf-8")
        }
        return mocked_request

    return factory


def test_valid(mocked_request_factory):
    auth = JWTAuthentication()
    is_authed = auth.authenticate(mocked_request_factory())
    assert is_authed == (None, None)


def test_expired(mocked_request_factory):
    auth = JWTAuthentication()

    with pytest.raises(AuthenticationFailed) as e:
        is_authed = auth.authenticate(mocked_request_factory(expired=True))
        assert "expire" in e.detail


def test_invalid():
    req = MockedRequest()
    req.META["Authorization"] = "Token foo"  # invalid token
    auth = JWTAuthentication()

    with pytest.raises(AuthenticationFailed) as e:
        is_authed = auth.authenticate(req)
        assert "invalid" in e.detail
