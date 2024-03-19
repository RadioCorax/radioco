from django.apps import AppConfig


class Programmes(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'radioco.programmes'

    def ready(self):
        from radioco.programmes import signals
