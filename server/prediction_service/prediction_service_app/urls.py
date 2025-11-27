from django.urls import path
from . import views

urlpatterns = [
    
    path("create-song/", views.create_song)
]
