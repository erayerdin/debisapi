from django.urls import reverse_lazy
from rest_framework import test

from . import results_requests_mock


def test_status(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    results_requests_mock,
):
    response = api_client.get(reverse_lazy("results_terms"))
    assert response.status_code == 200


def test_json(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    results_requests_mock,
):
    response = api_client.get(reverse_lazy("results_terms"))
    obj = response.json()[0]
    assert obj["id"] == "254"
    assert obj["name"] == "2018-2019 Bahar"
