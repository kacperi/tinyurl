from shortener.models import ShortLink


def test_generate_hash_same_input():
    url = "https://www.google.com/"
    sl1 = ShortLink(url)
    sl2 = ShortLink(url)
    assert sl1.generate_hash() == sl2.generate_hash()
