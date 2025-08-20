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
    main_image_url = serializers.SerializerMethodField()
    image1_url = serializers.SerializerMethodField()
    image2_url = serializers.SerializerMethodField()
    image3_url = serializers.SerializerMethodField()
    image4_url = serializers.SerializerMethodField()

    class Meta:
        model = TurfSpot
        fields = '__all__'
        extra_fields = [
            'main_image_url', 'image1_url', 'image2_url', 'image3_url', 'image4_url'
        ]

    def get_main_image_url(self, obj):
        if obj.main_image:
            return obj.main_image.url
        return None

    def get_image1_url(self, obj):
        if obj.image1:
            return obj.image1.url
        return None

    def get_image2_url(self, obj):
        if obj.image2:
            return obj.image2.url
        return None

    def get_image3_url(self, obj):
        if obj.image3:
            return obj.image3.url
        return None

    def get_image4_url(self, obj):
        if obj.image4:
            return obj.image4.url
        return None
