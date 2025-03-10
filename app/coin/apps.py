from django.apps import AppConfig


class CoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coin'

    def ready(self):
        import coin.admin.wallet
        import coin.admin.gift
        import coin.admin.transaction
        import coin.admin.event
        import coin.signals
