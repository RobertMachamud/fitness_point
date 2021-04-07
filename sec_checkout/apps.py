from django.apps import AppConfig


class SecCheckoutConfig(AppConfig):
    name = 'sec_checkout'

    def ready(self):
        import checkout.signals
