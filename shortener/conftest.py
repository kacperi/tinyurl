import pytest


@pytest.fixture
def google_url(scope="module") -> str:
    return "https://www.google.com/"
