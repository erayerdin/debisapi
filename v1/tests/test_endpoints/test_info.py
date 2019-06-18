from django.urls import reverse_lazy
from rest_framework import test

from v1.views.results import RESULTS_URL as URL

from .test_results import results_requests_mock


def test_status(
    api_client: test.APIClient, valid_user_requests_mock, results_requests_mock
):
    response = api_client.get(reverse_lazy("info"))
    assert response.status_code == 200


def test_data(
    api_client: test.APIClient, valid_user_requests_mock, results_requests_mock
):
    response = api_client.get(reverse_lazy("info"))
    assert response.json() == {
        "name": "ŞENAY ERDİN",
        "studentId": "2017742023",
        "officialClass": 2,
        "term": 4,
        "faculty": "İzmir Meslek Yüksekokulu",
        "department": "Yerel Yönetimler (İÖ)",
        "isRelative": True,
    }
