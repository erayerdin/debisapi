import pytest

from .auth import *
from .requests_mock import *


@pytest.fixture
def resource_factory(request):
    def factory(filename: str, mode="r"):
        file = open("debisapi/test_resources/{}".format(filename), mode)
        request.addfinalizer(lambda: file.close())
        return file

    return factory
