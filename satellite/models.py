from django.db import models

# Create your models here.
class Satellite(models.Model):
    name = models.CharField(max_length=24)
    tle_1 = models.CharField(max_length=80, blank=False, null=False)
    tle_2 = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField(default="",blank=True, null=True )
