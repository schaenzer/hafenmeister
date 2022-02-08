from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FluxConfig(AppConfig):
    name = "hafenmeister.sensors"
    verbose_name = _("Sensors")

    def ready(self):
        try:
            import hafenmeister.sensors.signals  # noqa F401
            import hafenmeister.sensors.tasks  # noqa F401
        except ImportError:
            pass
