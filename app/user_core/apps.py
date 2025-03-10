from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_core'
    verbose_name = _('Users and groups')

    def ready(self):
        import user_core.signals
