from rest_framework import serializers
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage, WhatsappNumber, CallNumber
from cloudinary.utils import cloudinary_url
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


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

    def _compress_image(self, file_obj, max_width=2000, max_bytes=10 * 1024 * 1024):
        try:
            file_obj.seek(0)
        except Exception:
            pass
        img = Image.open(file_obj)
        img_format = (img.format or 'JPEG').upper()
        if img_format not in ("JPEG", "JPG", "PNG", "WEBP"):
            img_format = "JPEG"
        # Convert to RGB for JPEG/WEBP if needed
        if img.mode in ("RGBA", "P") and img_format in ("JPEG", "JPG"):
            img = img.convert("RGB")
        # Resize if wider than max_width
        w, h = img.size
        if w > max_width:
            ratio = max_width / float(w)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        # Iteratively reduce quality to fit under max_bytes
        quality = 85
        min_quality = 60
        buffer = BytesIO()
        img.save(buffer, format="JPEG" if img_format in ("JPEG", "JPG") else img_format, optimize=True, quality=quality)
        while buffer.tell() > max_bytes and quality > min_quality:
            quality -= 5
            buffer.seek(0)
            buffer.truncate()
            img.save(buffer, format="JPEG" if img_format in ("JPEG", "JPG") else img_format, optimize=True, quality=quality)
        buffer.seek(0)
        # Build InMemoryUploadedFile
        filename = getattr(file_obj, 'name', f'upload.{img_format.lower()}')
        content_type = 'image/jpeg' if img_format in ("JPEG", "JPG") else f'image/{img_format.lower()}'
        compressed_file = InMemoryUploadedFile(
            buffer,
            field_name=None,
            name=filename,
            content_type=content_type,
            size=buffer.getbuffer().nbytes,
            charset=None
        )
        return compressed_file

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        turf = super().create(validated_data)

        for image in uploaded_images:
            try:
                image = self._compress_image(image)
            except Exception:
                pass
            TurfImage.objects.create(turf=turf, image=image)

        return turf

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        instance = super().update(instance, validated_data)

        if uploaded_images is not None:
            # optional: clear old images
            instance.images.all().delete()
            for image in uploaded_images:
                try:
                    image = self._compress_image(image)
                except Exception:
                    pass
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
