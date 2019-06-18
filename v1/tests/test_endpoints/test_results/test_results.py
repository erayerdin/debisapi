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
        reverse_lazy("results"), data={"termId": "0", "classId": "0"}
    )
    assert response.status_code == 200


def test_json_class(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    results_requests_mock,
):
    response = api_client.get(
        reverse_lazy("results"), data={"termId": "0", "classId": "0"}
    )
    assertion = {
        "code": "YÖN 4218",
        "name": "YEREL KAMU HİZMETLERİ",
        "faculty": "İzmir Meslek Yüksekokulu",
        "department": "Yerel Yönetimler (İÖ)",
        "branch": "A",
        "credit": 2,
        "isMandatory": True,
        "repetitionCount": 1,
        "lecturer": "DR. ELİF YÜCEBAŞ",
        "mandatoryParticipancy": True,
        "hasCompleted": False,
    }
    assert response.json()["class"] == assertion


def test_json_results(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    results_requests_mock,
):
    response = api_client.get(
        reverse_lazy("results"), data={"termId": "0", "classId": "0"}
    )
    assertion = [
        {
            "name": "Vize",
            "announcement": "08/05/2019",
            "median1": 80,
            "median2": None,
            "grade": "70",
        },
        {
            "name": "Rapor/Ödev",
            "announcement": None,
            "median1": None,
            "median2": None,
            "grade": None,
        },
        {
            "name": "Final",
            "announcement": None,
            "median1": None,
            "median2": None,
            "grade": None,
        },
        {
            "name": "Yarıyıl Sonu Başarı Notu",
            "announcement": None,
            "median1": None,
            "median2": None,
            "grade": None,
        },
        {
            "name": "Bütünleme Notu",
            "announcement": None,
            "median1": None,
            "median2": None,
            "grade": None,
        },
        {
            "name": "Bütünleme Sonu Başarı Notu",
            "announcement": None,
            "median1": None,
            "median2": None,
            "grade": None,
        },
    ]
    assert response.json()["results"] == assertion
