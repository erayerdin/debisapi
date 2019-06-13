import pytest
from django.urls import reverse_lazy
from rest_framework import test

from v1.views.curriculum import CURRICULUM_URL as URL

from .test_terms import curriculum_request_mock


def test_status(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(
        reverse_lazy("curriculum_weeks", kwargs={"term_id": "0"})
    )
    assert response.status_code == 200


def test_json(
    api_client: test.APIClient,
    token,
    valid_user_requests_mock,
    curriculum_request_mock,
):
    response = api_client.get(
        reverse_lazy("curriculum_weeks", kwargs={"term_id": "0"})
    )
    obj = response.json()[0]
    assert obj["id"] == "18/02/2019-23/02/2019"
    assert obj["name"] == "18/02/2019-23/02/2019"
