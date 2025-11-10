from rest_framework import serializers
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage, WhatsappNumber, CallNumber
from cloudinary.utils import cloudinary_url


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
    image = serializers.SerializerMethodField()

    class Meta:
        model = TurfImage
        fields = ["id", "image"]

    def get_image(self, obj):
        if not obj.image:
            return None
        public_id = getattr(obj.image, 'public_id', None)
        if not public_id:
            return obj.image.url
        url, _ = cloudinary_url(public_id, secure=True, transformation=[
            {"fetch_format": "auto", "quality": "auto"},
            {"crop": "limit", "width": 1600}
        ])
        return url


class WhatsappNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsappNumber
        fields = ["id", "number"]

class CallNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallNumber
        fields = ["id", "number"]


class TurfSerializer(serializers.ModelSerializer):
    pitch_type = PitchTypeSerializer(read_only=True)
    game_time = serializers.CharField()
    purposes = PurposeSerializer(many=True, read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    whatsapp_numbers = WhatsappNumberSerializer(many=True, read_only=True)
    call_numbers = CallNumberSerializer(many=True, read_only=True)
    images = TurfImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(help_text="Images are optimized automatically on delivery"),
        write_only=True,
        required=False,
        help_text="Images are optimized automatically on delivery"
    )
    class Meta:
        model = Turf
        fields = [
            "id", "name", "pitch_description", "pitch_type", "price_per_hour",
            "game_time", "purposes", "facilities",
            "location", "latitude", "longitude", "map_link", "whatsapp_numbers",
            "call_numbers", "images", "uploaded_images", "created_at"
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

    # No size validation: we optimize on delivery via Cloudinary transformations


class TurfListSerializer(serializers.ModelSerializer):
    pitch_type = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()
    price = serializers.IntegerField(source='price_per_hour', read_only=True)

    class Meta:
        model = Turf
        fields = ["id", "name", "pitch_type", "location", "latitude", "longitude", "image", "price"]

    def get_image(self, obj):
        # return first image (optimized) or None
        first = obj.images.first()
        if not first or not first.image:
            return None
        public_id = getattr(first.image, 'public_id', None)
        if not public_id:
            return first.image.url
        url, _ = cloudinary_url(public_id, secure=True, transformation=[
            {"fetch_format": "auto", "quality": "auto"},
            {"crop": "limit", "width": 800}
        ])
        return url
