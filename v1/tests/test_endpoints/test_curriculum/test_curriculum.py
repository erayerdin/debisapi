from django.urls import reverse_lazy
from rest_framework import test

from .test_terms import curriculum_request_mock


def test_status(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(
        reverse_lazy("curriculum"), data={"termId": "0", "weekId": "0"}
    )
    assert response.status_code == 200


def test_status_no_term_or_week(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(reverse_lazy("curriculum"))
    assert response.status_code == 400


def test_json(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(
        reverse_lazy("curriculum"), data={"termId": "0", "weekId": "0"}
    )
    data = response.json()[0]

    assert data == {
        "fromHour": "17:00",
        "toHour": "17:45",
        "day": 1,
        "department": "Yerel Yönetimler (İÖ)",
        "code": "YÖN 4212",
        "name": "MESLEKİ SEMİNER 2",
        "branch": "A",
        "is_theoric": True,
        "lecturer": "DOÇ.DR. RABİA BAHAR ÜSTE",
        "location": "B Blok ED-K1-13",
    }
