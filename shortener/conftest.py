import pytest


@pytest.fixture
def google_url(scope="module"):
    return "https://www.google.com/"
