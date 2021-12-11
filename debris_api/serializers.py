from debris.models import Debris
from rest_framework import serializers

class DebrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debris
        fields = "__all__"