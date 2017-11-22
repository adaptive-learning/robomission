from django.apps import AppConfig


class LearnConfig(AppConfig):
    name = 'learn'

    def ready(self):
        # Register signal handlers by importing signals module.
        # (Recommended by the official documentation:
        # https://docs.djangoproject.com/en/1.11/topics/signals/)
        import learn.signals
