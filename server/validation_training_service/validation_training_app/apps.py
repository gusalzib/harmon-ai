from django.apps import AppConfig


class ValidationTrainingServiceConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "validation_training_app"