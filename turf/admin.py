from django.contrib import admin
from .models import TurfSpot

@admin.register(TurfSpot)
class TurfSpotAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'turf_type', 'distance', 'location']
    search_fields = ['name', 'location', 'turf_type']
    list_filter = ['status', 'turf_type']
