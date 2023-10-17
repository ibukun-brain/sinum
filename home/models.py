import auto_prefetch

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from sinum.utils.managers import UserManager
from sinum.utils.models import TimeBasedModel

from sinum.utils.media import MediaHelper


class CustomUser(TimeBasedModel, AbstractBaseUser, PermissionsMixin):
    """
    CustomUser models which includes GeoLocation info such as ip_address,
    longitude, latitude and others not provided by django User Model
    """
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=50, unique=True)
    mobile_no = models.CharField(
        max_length=11,
        blank=True,
    )
    profile_pic = models.ImageField(
        blank=True,
        upload_to=MediaHelper.get_image_upload_path
    )
    university = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        blank=True, null=True
    )

    objects = UserManager()

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["-date_joined"]
        verbose_name = "user"
        indexes = [
            models.Index(fields=['date_joined']),
        ]

    def __str__(self):
        """
        Returns a string representation of the CustomUser model
        """
        return self.email or self.username

    @property
    def is_vendor(self):
        """
        Return true if user is a registered vendor
        """
        return hasattr(self, "vendor")

    @property
    def image_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return f"http://localhost:8000/{settings.STATIC_URL}avatars/placeholder.jpg"


class AddressBook(TimeBasedModel):
    user = auto_prefetch.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user'
    )
    phone_no = models.CharField(
        max_length=11,
        blank=True
    )
    additional_phone_no = models.CharField(
        max_length=11,
        blank=True
    )
    delivery_address = models.CharField(max_length=225, blank=True)
    default_address = models.BooleanField(default=False)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    town = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} -> {self.delivery_address}"
