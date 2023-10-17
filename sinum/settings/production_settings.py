import dj_database_url

from sinum.settings.base_settings import *
from sinum.settings.local.email_settings import *

from sinum.settings.packages.aws_settings import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(get_env_variable("DEBUG", "0"))

INSTALLED_APPS.append("storages")

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES["default"] = dj_database_url.parse(
    get_env_variable("PROD_DATABASE_URL"), conn_max_age=600
)

DATABASES["default"]["NAME"] = get_env_variable(
    "DATABASE_NAME", "sinum")
DATABASES["default"]["ENGINE"] = "dj_db_conn_pool.backends.postgresql"
DATABASES["default"]["POOL_OPTIONS"] = {
    "POOL_SIZE": 20,
    "MAX_OVERFLOW": 30,
    "RECYCLE": 24 * 60 * 60,
}

MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")

MEDIA_URL = "/uploads/"

MEDIA_ROOT = get_env_variable("MEDIA_ROOT", BASE_DIR / "sinum/media")

STATIC_ROOT = BASE_DIR / "static_root"

STATICFILES_DIRS = [
    BASE_DIR / "assets",
]

CSRF_TRUSTED_ORIGINS = [
    "http://*.herokuapp.com",
    "http://*.sinum.com",
    "https://*.herokuapp.com",
    "https://*.sinum.com",
]
