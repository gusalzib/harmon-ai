"""
<<<<<<<< HEAD:server/prediction_service/prediction_service_backend/asgi.py
ASGI config for prediction_service_backend project.
========
ASGI config for users_project project.
>>>>>>>> 01d1d59ccfd11f8f91c721701a0ef1d776f495c4:server/users_project/users_project/asgi.py

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<<< HEAD:server/prediction_service/prediction_service_backend/asgi.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prediction_service_backend.settings")
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings')
>>>>>>>> 01d1d59ccfd11f8f91c721701a0ef1d776f495c4:server/users_project/users_project/asgi.py

application = get_asgi_application()
