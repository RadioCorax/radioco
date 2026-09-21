from django.apps import AppConfig


class Schedules(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'radioco.schedules'

    def ready(self):
        from radioco.schedules import signals
