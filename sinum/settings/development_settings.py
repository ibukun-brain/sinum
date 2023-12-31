import dj_database_url

from sinum.settings.base_settings import *
from sinum.settings.local.mailhog_settings import *
from sinum.settings.packages.cors_origin_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e1jb$w%@5d^3&lv%0@r@ccu+gkv())12a&obao#wzqtcaqrn9_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = True

CSRF_TRUSTED_ORIGINS = ["http://*"]

X_FRAME_OPTIONS = "SAMEORIGIN"

DATABASES["default"] = dj_database_url.parse(
    f"sqlite:////{BASE_DIR.joinpath(BASE_DIR.name)}.db", conn_max_age=600,
)

DISABLE_SERVER_SIDE_CURSORS = True

INSTALLED_APPS += [
    "debug_toolbar",
    "crispy_forms",
    "crispy_bootstrap3",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"

CRISPY_TEMPLATE_PACK = "bootstrap3"

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
