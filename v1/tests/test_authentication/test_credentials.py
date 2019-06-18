import pytest
from rest_framework.exceptions import AuthenticationFailed

from v1.authentication import CredentialsAuthentication

from .test_jwt import mocked_request_factory


def test_valid_user(valid_user_requests_mock, mocked_request_factory):
    auth = CredentialsAuthentication()
    assert auth.authenticate(mocked_request_factory()) == (None, None)


def test_invalid_user(invalid_user_requests_mock, mocked_request_factory):
    auth = CredentialsAuthentication()

    with pytest.raises(AuthenticationFailed) as e:
        auth.authenticate(mocked_request_factory())
        assert "invalid" in e.detail
