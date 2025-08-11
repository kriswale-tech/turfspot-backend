from django.contrib import admin
from .models import TurfSpot, PitchType, GameTime, Purpose, Facility


@admin.register(TurfSpot)
class TurfSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'pitch_type', 'price_per_hour', 'location')
    search_fields = ('name', 'location')
    list_filter = ('pitch_type', 'game_time', 'purpose')


admin.site.register(PitchType)
admin.site.register(GameTime)
admin.site.register(Purpose)
admin.site.register(Facility)
