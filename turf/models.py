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


class WhatsappNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.number

class CallNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.number


class Turf(models.Model):
    name = models.CharField(max_length=100)
    pitch_description = models.TextField(blank=True, null=True)
    pitch_type = models.ForeignKey(PitchType, on_delete=models.SET_NULL, null=True)
    price_per_hour = models.IntegerField()

    game_time = models.TextField(blank=True, null=True, help_text="Enter opening hours, e.g.:\n🔒 Open Monday - Friday (6AM - 11PM)\nOpen Saturdays & Sundays (8AM - 11PM)")
    purposes = models.ManyToManyField(Purpose, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)
    whatsapp_numbers = models.ManyToManyField(WhatsappNumber, blank=True)
    call_numbers = models.ManyToManyField(CallNumber, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TurfImage(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("image")  # stored in Cloudinary
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.turf.name} - {self.image.url if self.image else 'No image'}"