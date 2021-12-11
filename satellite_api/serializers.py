from satellite.models import Satellite
from rest_framework import serializers
from satellite.models import Satellite

class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = "__all__"