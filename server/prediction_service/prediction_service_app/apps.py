from django.apps import AppConfig


class PredictionserviceConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "prediction_service_app"
