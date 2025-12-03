from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'users_app'
