from rest_framework import serializers
from .models import TurfSpot

class TurfSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfSpot
        fields = '__all__'
