from django.urls import path
from . import views

urlpatterns = [
    
    path("create-song/", views.create_song),
    path("update_song/", views.update_song),
    path("get_specific_song/", views.get_specific_song),
    path("get_artists_songs/", views.get_artists_songs)
]
