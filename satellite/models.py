from django.db import models

# Create your models here.
class Satellite(models.Model):
    name = models.CharField(max_length=24, primary_key=True)
    tle_1 = models.CharField(max_length=80, blank=False, null=False)
    tle_2 = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField(default="",blank=True, null=True )
    norad = models.CharField(max_length=5)
    classification = models.CharField(max_length=1)
    international_designation = models.CharField(max_length=6)
    epoch_year = models.IntegerField()
    epoch_day = models.DecimalField(decimal_places= 8, max_digits=11) 
    first_derivative_mean_motion = models.DecimalField(decimal_places=20, max_digits=20)
    second_derivative_mean_motion = models.DecimalField(decimal_places=20, max_digits=20)
    bstar =  models.DecimalField(decimal_places=10, max_digits=10)
    set_number = models.IntegerField()
    inclination = models.DecimalField(max_digits=10, decimal_places=4)
    raan = models.DecimalField(max_digits=10, decimal_places=4)
    eccentricity = models.DecimalField(max_digits=20, decimal_places=10)
    argp = models.DecimalField(max_digits=10, decimal_places=4)
    mean_anomaly = models.DecimalField(max_digits=10, decimal_places=4)
    mean_motion = models.DecimalField(max_digits=10, decimal_places=8)
    rev_num = models.IntegerField()
