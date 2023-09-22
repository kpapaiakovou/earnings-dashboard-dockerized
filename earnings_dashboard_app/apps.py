from django.apps import AppConfig


class EarningsDashboardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'earnings_dashboard_app'

    def ready(self):
        import earnings_dashboard_app.signals
