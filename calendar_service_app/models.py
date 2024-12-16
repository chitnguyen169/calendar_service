from django.db import models


# Create your models here.
class Event(models.Model):
    description = models.TextField()
    time = models.DateTimeField()
