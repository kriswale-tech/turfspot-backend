from django.contrib import admin
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage, WhatsappNumber, CallNumber


class TurfImageInline(admin.TabularInline):  # or StackedInline
    model = TurfImage
    extra = 1


class WhatsappNumberInline(admin.TabularInline):
    model = Turf.whatsapp_numbers.through
    extra = 1

class CallNumberInline(admin.TabularInline):
    model = Turf.call_numbers.through
    extra = 1


@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    list_display = ("name", "pitch_type", "price_per_hour", "location", "created_at")
    inlines = [TurfImageInline]
    #exclude = ("whatsapp_numbers", "call_numbers")


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


@admin.register(WhatsappNumber)
class WhatsappNumberAdmin(admin.ModelAdmin):
    list_display = ("number",)

@admin.register(CallNumber)
class CallNumberAdmin(admin.ModelAdmin):
    list_display = ("number",)
