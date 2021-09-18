from django.db import models
from django.db.models.fields import DecimalField

# Create your models here.
class Satellite(models.Model):
    name = models.CharField(max_length=24)
    long = models.DecimalField(max_digits=5,decimal_places=2, null=False, blank=False)
    lat = models.DecimalField(max_digits=5,decimal_places=2, null=False, blank=False)
    active = models.BooleanField(default=False)