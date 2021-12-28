from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FluxConfig(AppConfig):
    name = "hafenmeister.flux"
    verbose_name = _("FluxCD")

    def ready(self):
        try:
            import hafenmeister.users.signals  # noqa F401
        except ImportError:
            pass
