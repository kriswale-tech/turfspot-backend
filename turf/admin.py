from django.contrib import admin
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage


class TurfImageInline(admin.TabularInline):  # or StackedInline
    model = TurfImage
    extra = 1


@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    list_display = ("name", "pitch_type", "price_per_hour", "location", "created_at")
    inlines = [TurfImageInline]


@admin.register(PitchType)
class PitchTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(GameTime)
class GameTimeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name",)
