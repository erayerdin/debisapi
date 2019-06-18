import pytest
from django.urls import reverse_lazy
from rest_framework import test

from v1.views.curriculum import CURRICULUM_URL as URL


@pytest.fixture
def curriculum_request_mock(requests_mock, resource_factory):
    requests_mock.post(URL, text=resource_factory("curriculum.html").read())


def test_status(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(reverse_lazy("curriculum_terms"))
    assert response.status_code == 200


def test_json(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(reverse_lazy("curriculum_terms"))
    obj = response.json()[0]
    assert obj["id"] == "254"
    assert obj["name"] == "2018-2019 Bahar"
