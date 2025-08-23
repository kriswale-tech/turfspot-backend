from django.db import models
from cloudinary.models import CloudinaryField


class PitchType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class GameTime(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Turf(models.Model):
    name = models.CharField(max_length=100)
    pitch_type = models.ForeignKey(PitchType, on_delete=models.SET_NULL, null=True)
    price_per_hour = models.IntegerField()

    game_time = models.ForeignKey(GameTime, on_delete=models.SET_NULL, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True)

    facilities = models.ManyToManyField(Facility, blank=True)

    location = models.CharField(max_length=255, blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)

    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    call_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TurfImage(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("image")  # stored in Cloudinary
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.turf.name} - {self.image.url if self.image else 'No image'}"