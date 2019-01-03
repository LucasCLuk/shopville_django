from django.apps import AppConfig


class ShopVilleConfig(AppConfig):
    name = 'shopville'

    def ready(self):
        from . import signals
        super(ShopVilleConfig, self).ready()
