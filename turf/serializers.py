from rest_framework import serializers
from .models import TurfSpot, PitchType, GameTime, Purpose, Facility


class PitchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchType
        fields = '__all__'


class GameTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTime
        fields = '__all__'


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class TurfSpotSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)
    facilities_ids = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(),
        many=True,
        write_only=True,
        source='facilities'
    )

    class Meta:
        model = TurfSpot
        fields = '__all__'
