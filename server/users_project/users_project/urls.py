"""
<<<<<<<< HEAD:server/prediction_service/prediction_service_backend/urls.py
URL configuration for prediction_service_backend project.
========
URL configuration for users_project project.
>>>>>>>> 01d1d59ccfd11f8f91c721701a0ef1d776f495c4:server/users_project/users_project/urls.py

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
<<<<<<<< HEAD:server/prediction_service/prediction_service_backend/urls.py

#from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path("admin/", admin.site.urls),
    path("api/",include("prediction_service_app.urls"))
========
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', include("users_app.urls")),
    path('admin/', admin.site.urls)
>>>>>>>> 01d1d59ccfd11f8f91c721701a0ef1d776f495c4:server/users_project/users_project/urls.py
]
