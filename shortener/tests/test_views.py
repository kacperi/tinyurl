import pytest
from django.urls import reverse

from shortener.models import ShortLink
from shortener.tests.factories import ShortLinkFactory


@pytest.mark.django_db
def test_create_shortlink_success(client: "django.test.Client", google_url: str) -> None:
    response = client.post(
        reverse("create_shortlink"),
        data={"url": google_url},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.json()
    assert "link" in data
    sl_hash = data["link"].split("/")[-1]
    sl = ShortLink.objects.get(hash=sl_hash)
    assert sl.hash == sl_hash and sl.url == google_url


def test_create_shortlink_no_url(client: "django.test.Client") -> None:
    response = client.post(
        reverse("create_shortlink"),
        data={"url": ""},
        content_type="application/json",
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Missing url in the request"


def test_create_shortlink_missing_jon(client: "django.test.Client") -> None:
    response = client.post(
        reverse("create_shortlink"),
        data="",
        content_type="application/json",
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Invalid JSON"


@pytest.mark.django_db
def test_create_shortlink_avoids_duplicates(client: "django.test.Client") -> None:
    sl = ShortLinkFactory.create()
    response = client.post(
        reverse("create_shortlink"),
        data={"url": sl.url},
        content_type="application/json",
    )

    assert response.status_code == 200
    response_hash = response.json()["link"].split("/")[-1]
    assert ShortLink.objects.filter(hash=response_hash).count() == 1


def test_create_shortlink_get(client: "django.test.Client") -> None:
    response = client.get(
        reverse("create_shortlink"),
    )
    assert response.status_code == 405


@pytest.mark.django_db
def test_redirect_success(client: "django.test.Client") -> None:
    sl = ShortLinkFactory.create()
    response = client.get(reverse("redirect", kwargs={"hash": sl.hash}))
    assert response.status_code == 302
    assert response.url == sl.url


def test_redirect_no_hash(client: "django.test.Client") -> None:
    response = client.get(reverse("redirect_empty"))
    assert response.status_code == 200
    assert response.template_name == ["empty_hash.html"]


@pytest.mark.django_db
def test_redirect_to_page_withour_scheme(client: "django.test.Client") -> None:
    sl = ShortLink(url="google.pl")
    sl.save()
    response = client.get(reverse("redirect", kwargs={"hash": sl.hash}))
    assert response.status_code == 302
    assert response.url == "https://" + sl.url


@pytest.mark.django_db
def test_redirect_post(client: "django.test.Client") -> None:
    sl = ShortLinkFactory.create()
    response = client.post(
        reverse("redirect", kwargs={"hash": sl.hash}),
        data={"hash": sl.hash},
        content_type="application/json",
    )
    assert response.status_code == 405


@pytest.mark.django_db
def test_redirect_invalid_hash(client: "django.test.Client") -> None:
    invalid_hash = "xyz"
    assert not ShortLink.objects.filter(hash=invalid_hash).exists()
    response = client.get(reverse("redirect", kwargs={"hash": invalid_hash}))
    assert response.status_code == 404
    assert response.templates[0].name == "invalid_hash.html"
    assert response.context["hash"] == invalid_hash
