import hashlib

from django.db import models


# Create your models here.
class ShortLink(models.Model):
    hash = models.CharField(max_length=16, primary_key=True, editable=False)
    url = models.URLField()

    def generate_hash(self) -> str:
        return hashlib.sha256(self.url.encode("utf-8")).hexdigest()[:16]

    def save(self, *args, **kwargs) -> None:
        if not self.hash:
            self.hash = self.generate_hash()
        super().save(*args, **kwargs)
