from django.db import models


class Gender(models.TextChoices):
    Male = ("M", "Male")
    Female = ("F", "Female")


class PublishedStatus(models.TextChoices):
    Draft = ("draft", "Draft")
    Published = ("published", "Published")
