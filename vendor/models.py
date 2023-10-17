import uuid
import auto_prefetch

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from sinum.utils.choices import Gender
from sinum.utils.models import (
    NamedTimeBasedModel,
    TimeBasedModel
)
from sinum.utils.media import MediaHelper


class Vendor(TimeBasedModel):
    user = auto_prefetch.OneToOneField(
        "home.CustomUser",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=50, choices=Gender.choices,
        default=Gender.Male
    )
    image = models.ImageField(
        blank=True,
        upload_to=MediaHelper.get_image_upload_path
    )
    date_of_birth = models.DateField()
    verified_date = models.DateField(null=True, blank=True)
    nin_number = models.CharField(max_length=11)
    bvn = models.CharField(max_length=10)
    account_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name() or self.user.email

    def clean_fields(self, exclude=None):
        if self.verified_date is None:
            raise ValidationError(
                "Vendor cannot be verified if verified date is not set"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class VendorStore(NamedTimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    vendor = auto_prefetch.OneToOneField(
        Vendor,
        on_delete=models.CASCADE
    )
    description = models.TextField(
        blank=True
    )
    image = models.ImageField(
        blank=True,
        upload_to=MediaHelper.get_image_upload_path
    )

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_at"])
        ]

    def ___str__(self):
        return f"{self.vendor} store"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"http://localhost:8000/{settings.STATIC_URL}avatars/placeholder.jpg"
