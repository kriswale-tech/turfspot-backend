from rest_framework import serializers
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage


class PitchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchType
        fields = "__all__"


class GameTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTime
        fields = "__all__"


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = "__all__"


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class TurfImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfImage
        fields = ["id", "image"]


class TurfSerializer(serializers.ModelSerializer):
    pitch_type = PitchTypeSerializer(read_only=True)
    game_time = GameTimeSerializer(read_only=True)
    purpose = PurposeSerializer(read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)

    # Related images
    images = TurfImageSerializer(many=True, read_only=True)

    # For uploading multiple images in one request
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Turf
        fields = [
            "id", "name", "pitch_type", "price_per_hour",
            "game_time", "purpose", "facilities",
            "location", "map_link", "whatsapp_number",
            "call_number", "images", "uploaded_images", "created_at"
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        turf = super().create(validated_data)

        for image in uploaded_images:
            TurfImage.objects.create(turf=turf, image=image)

        return turf

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        instance = super().update(instance, validated_data)

        if uploaded_images is not None:
            # optional: clear old images
            instance.images.all().delete()
            for image in uploaded_images:
                TurfImage.objects.create(turf=instance, image=image)

        return instance


class TurfListSerializer(serializers.ModelSerializer):
    pitch_type = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Turf
        fields = ["id", "name", "pitch_type", "location", "image"]

    def get_image(self, obj):
        # return first image (or None)
        first = obj.images.first()
        return first.image.url if first else None
