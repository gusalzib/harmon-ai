"""
<<<<<<<< HEAD:server/prediction_service/prediction_service_backend/wsgi.py
WSGI config for harmonai_backend project.
========
WSGI config for users_project project.
>>>>>>>> 01d1d59ccfd11f8f91c721701a0ef1d776f495c4:server/users_project/users_project/wsgi.py

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<<< HEAD:server/prediction_service/prediction_service_backend/wsgi.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prediction_service_backend.settings")
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings')
>>>>>>>> 01d1d59ccfd11f8f91c721701a0ef1d776f495c4:server/users_project/users_project/wsgi.py

application = get_wsgi_application()
