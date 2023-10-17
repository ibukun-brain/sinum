from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from djoser.signals import user_registered

from sinum.utils.functions import get_user_ip_address

User = get_user_model()


@receiver(signal=user_registered)
def save_user_ip_address_after_sign_up(user, request, **kwargs):
    user = User.objects.get(email=user.email)
    user.ip_address = get_user_ip_address(request)
    user.save()


@receiver(signal=user_logged_in)
def save_user_ip_address_after_login(sender, user, request, **kwargs):
    user = User.objects.get(email=user.email)
    user.ip_address = get_user_ip_address(request)
    user.save()
