from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

from sinum.utils.urls import get_url
from vendor.models import Vendor, VendorStore


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'vendor_email', 'gender',
        'date_of_birth', 'verified_date', 'nin_number',
        'bvn'
    ]
    search_fields = ['first_name', 'last_name']
    list_filters = ['created_at', 'gender', 'verified_date']
    autocomplete_fields = ['user']
    list_display_links = ['first_name']
    date_hierarchy = 'created_at'

    def vendor_email(self, obj):
        return obj.user.email
    vendor_email.short_description = 'email'

    def log_addition(self, request, obj, message):
        user = obj.user
        url = get_url(request, "vendor:vendor-detail")

        msg = (
            f"Hi {user}\n"
            + "Your vendor account has just been created.\n\n"
            + f"Please visit {url} to update your vendor profile "
            + "so you can start getting bookings from students.\n\n"
            + "Kind Regards\n"
            + "Sinum team"
        )

        send_mail(
            subject="Sinum - Vendor profile created",
            message=msg,
            fail_silently=False,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        log_entry = super().log_addition(request, obj, message)
        return log_entry


@admin.register(VendorStore)
class VendorStoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor']
    list_filter = ['created_at', 'updated_at']
    autocomplete_fields = ['vendor']
    date_hierarchy = 'created_at'
    search_fields = [
        'name',
        'vendor__email',
        'vendor__first_name',
        'vendor__last_name',
    ]
    readonly_fields = ['uid']
