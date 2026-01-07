# Authors of code:
# - 

from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100,null=True, blank=True)
    artist = models.CharField(max_length=100,null=True, blank=True)
    genre = models.CharField(max_length=100,null=True, blank=True)
    tempo = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    user_rating = models.FloatField(null=True, blank=True)
    added_by = models.CharField(max_length=100,null=True, blank=True)
    columns = models.CharField(max_length = 100,null=True, blank=True)
    chromogram = models.JSONField(null=True, blank=True) #this should store a 2D array
    prediction = models.JSONField(null=True, blank=True) 


    # these are the columns of the chromogram:
    # "timestamps": [],
    # "C": [],
    # "C#": [],
    # "D": [],
    # "D#": [],
    # "E": [],
    # "F": [],
    # "F#": [],
    # "G": [],
    # "G#": [],
    # "A": [],
    # "A#": [],
    # "B": []

