from django.urls import reverse_lazy
from rest_framework import test

from . import results_requests_mock


def test_status(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    results_requests_mock,
):
    response = api_client.get(
        reverse_lazy("results_klasses"), data={"termId": "0"}
    )
    assert response.status_code == 200


def test_json(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    results_requests_mock,
):
    response = api_client.get(
        reverse_lazy("results_klasses"), data={"termId": "0"}
    )
    data = response.json()[0]
    assert data["id"] == "A__1_8952_151_2_"
    assert data["name"] == "YÖN 4218 YEREL KAMU HİZMETLERİ"
