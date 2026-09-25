from django.conf import settings
from django.core.wsgi import get_wsgi_application
from environs import Env

from radioco import settings as default_settings

env = Env(prefix="RADIOCO_")

settings.configure(
    default_settings,
    DEBUG=env.bool("DEBUG", default=False),
    TEMPLATE_DEBUG=env.bool("TEMPLATE_DEBUG", default=False),
    SECRET_KEY=env("SECRET_KEY"),
    DATABASES={"default": env.dj_db_url("DATABASE_URL")},
    ALLOWED_HOSTS=env.list("ALLOWED_HOSTS"),
    CSRF_TRUSTED_ORIGINS=env.list("CSRF_TRUSTED_ORIGINS"),
    TIME_ZONE=env("TIME_ZONE", default="Europe/Berlin"),
    LANGUAGE_CODE=env("LANGUAGE_CODE", default="de"),
    LOGGING={
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": env.log_level("LOG_LEVEL", default="INFO"),
            },
        },
    },
    **env.dj_email_url("EMAIL_URL"),
)

application = get_wsgi_application()
