from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from home.models import CustomUser, AddressBook


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "mobile_no",
                )
            },
        ),
        (
            _("Geographic Location info"),
            {
                "fields": (
                    "ip_address",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": (
                "wide",), "fields": (
                "email",
                "password1", "password2"),
            },),
    )

    list_display = [
        "first_name",
        "last_name",
        "mobile_no",
        "email",
        "is_superuser",
        "is_staff",
    ]
    list_display_links = ["first_name", "email"]
    list_filter = ["date_joined"]


@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'delivery_address', 'phone_no',
        'default_address', 'state', 'city',
        'town'
    ]
    list_filter = ['default_address', 'created_at', 'updated_at']
    search_fields = [
        'user__first_name', 'user__email',
        'user__mobile_no', 'phone_no',
        'delivery_address'
    ]
    list_select_related = ['user']
    raw_id_fields = ['user']
