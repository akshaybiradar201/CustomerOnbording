from django.apps import AppConfig


class PraveshConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pravesh'

    def ready(self):
        import pravesh.signals
