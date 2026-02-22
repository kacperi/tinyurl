import factory

from shortener.models import ShortLink


class ShortLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShortLink

    url = factory.Faker("url")
