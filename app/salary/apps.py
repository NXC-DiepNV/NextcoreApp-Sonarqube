from django.apps import AppConfig, apps
from django.core.exceptions import ImproperlyConfigured

class SalaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salary'
    

    def ready(self):
        import salary.admin.salary

        required_apps = ["user_core", "contract", "attendance"]
        for app in required_apps:
            if not apps.is_installed(app):
                raise ImproperlyConfigured(f"The 'salary' application requires '{app}' to be installed first.")
