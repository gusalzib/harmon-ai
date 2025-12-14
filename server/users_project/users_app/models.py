from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Preferences(models.Model):
    darkmode = models.BooleanField(default=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.OneToOneField(Preferences, on_delete=models.CASCADE)
