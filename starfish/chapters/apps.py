from django.apps import AppConfig


class ChaptersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chapters'

    def ready(self):
        import chapters.rules
        import chapters.signals
