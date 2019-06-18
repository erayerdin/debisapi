import pytest

from v1.views.results import RESULTS_URL


@pytest.fixture
def results_requests_mock(requests_mock, resource_factory):
    resource = resource_factory("results.html")
    requests_mock.post(RESULTS_URL, text=resource.read())
