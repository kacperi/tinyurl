import hashlib

import pytest

from shortener.models import ShortLink
from shortener.tests.factories import ShortLinkFactory


def test_generate_hash_same_input_same_output(google_url: str) -> None:
    sl1 = ShortLink(url=google_url)
    sl2 = ShortLink(url=google_url)
    assert sl1.generate_hash() == sl2.generate_hash()


@pytest.mark.parametrize(
    "input_url",
    [
        "",
        "google.com",
        "google" + "e" * 500 + ".com",
        "भारत.कॉम",
    ],
)
def test_generate_hash_lengh_always_16(input_url: str) -> None:
    sl = ShortLink(url=input_url)
    assert len(sl.generate_hash()) == 16


def test_generate_hash_returns_correctly_encoded_str(google_url: str) -> None:
    sl = ShortLink(url=google_url)
    assert (
        sl.generate_hash() == hashlib.sha256(google_url.encode("utf-8")).hexdigest()[:16]
    )


def test_repr(google_url: str) -> None:
    sl = ShortLink(url=google_url)
    sl.hash = sl.generate_hash()
    assert f"<{sl.url} -- {sl.hash}>" == repr(sl)


@pytest.mark.django_db
def test_save_generates_hash() -> None:
    sl = ShortLinkFactory.build()
    assert sl.url and not sl.hash
    sl.save()
    assert sl.url and sl.hash


@pytest.mark.django_db
def test_save_doesnt_override_hash() -> None:
    sl = ShortLinkFactory.build()
    initial_hash = "xyz"
    assert initial_hash
    sl.hash = initial_hash
    sl.save()
    assert sl.hash == initial_hash


@pytest.mark.django_db
def test_save_stores_object_correctly() -> None:
    sl = ShortLinkFactory.build()
    sl_hash = sl.generate_hash()
    assert not ShortLink.objects.filter(hash=sl_hash).exists()
    sl.save()
    assert sl_hash == sl.hash
    assert ShortLink.objects.filter(hash=sl_hash).exists()
