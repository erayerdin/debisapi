import json

import pytest
from django import test
from django.urls import reverse_lazy


@pytest.fixture
def user_data():
    return {"username": "foo", "password": "bar"}


def test_status_login_success(
    client: test.Client, valid_user_requests_mock, user_data
):
    response = client.post(reverse_lazy("token_claim"), data=user_data)
    assert response.status_code == 200


def test_data_login_success(
    client: test.Client, valid_user_requests_mock, user_data
):
    response = client.post(reverse_lazy("token_claim"), data=user_data)
    data = json.loads(response.content.decode("utf-8"))
    assert "token" in data


def test_status_login_fail(
    client: test.Client, invalid_user_requests_mock, user_data
):
    response = client.post(reverse_lazy("token_claim"), data=user_data)
    assert response.status_code == 401


def test_data_login_fail(
    client: test.Client, invalid_user_requests_mock, user_data
):
    response = client.post(reverse_lazy("token_claim"), data=user_data)
    data = json.loads(response.content.decode("utf-8"))
    assert "detail" in data
