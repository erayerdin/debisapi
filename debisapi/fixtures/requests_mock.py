import pytest


@pytest.fixture
def valid_user_requests_mock(requests_mock):
    requests_mock.post("http://debis.deu.edu.tr/debis.php", text="")


@pytest.fixture
def invalid_user_requests_mock(requests_mock):
    requests_mock.post("http://debis.deu.edu.tr/debis.php", text="hatal")
