from django.contrib import admin
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage, WhatsappNumber, CallNumber
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings


class TurfImageAdminForm(forms.ModelForm):
    class Meta:
        model = TurfImage
        fields = "__all__"
        help_texts = {
            "image": "Upload images (max 2MB per image)",
        }

    def clean_image(self):
        img = self.cleaned_data.get("image")
        if hasattr(img, "size") and img.size is not None:
            if img.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Each image must be 2MB or smaller.")
        return img


class TurfImageInline(admin.StackedInline):  # use StackedInline to show help_text
    model = TurfImage
    extra = 1
    form = TurfImageAdminForm
    class Media:
        js = (
            'turf/image_size_validator.js',
        )


class WhatsappNumberInline(admin.TabularInline):
    model = Turf.whatsapp_numbers.through
    extra = 1

class CallNumberInline(admin.TabularInline):
    model = Turf.call_numbers.through
    extra = 1


class TurfAdminForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = "__all__"

@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    form = TurfAdminForm
    list_display = ("name", "pitch_type", "price_per_hour", "location", "latitude", "longitude", "created_at")
    inlines = [TurfImageInline]
    #exclude = ("whatsapp_numbers", "call_numbers")

    readonly_fields = ("location_map",)

    fieldsets = (
        (None, {
            'fields': (
                "name",
                "pitch_description",
                "pitch_type",
                "price_per_hour",
                "game_time",
                "purposes",
                "facilities",
                "whatsapp_numbers",
                "call_numbers",
                "location",
                "map_link",
                "location_map",  # interactive map
                "latitude",
                "longitude",
            )
        }),
    )

    def location_map(self, obj):
        lat = obj.latitude if obj and obj.latitude is not None else 5.6037  # Accra default
        lng = obj.longitude if obj and obj.longitude is not None else -0.1870
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
        html = f'''
            <div>
              <div id="turf-location-map" data-lat="{lat}" data-lng="{lng}" style="width:100%;height:360px;border:1px solid #ddd;border-radius:6px;"></div>
              <small>Drag the marker or click on the map. It will update the Latitude/Longitude fields below.</small>
              <script>
                (function(){{
                  function loadScript(src, onload){{
                    if (document.querySelector('script[src^="https://maps.googleapis.com/maps/api/js"]')) {{ onload && onload(); return; }}
                    var s = document.createElement('script');
                    s.src = src; s.async = true; s.defer = true; s.onload = onload; document.head.appendChild(s);
                  }}
                  var init = function(){{ if (window.TurfLocationPicker) {{ window.TurfLocationPicker.init('#turf-location-map'); }} }};
                  var key = '{api_key}';
                  var url = 'https://maps.googleapis.com/maps/api/js' + (key ? ('?key=' + key) : '');
                  loadScript(url, init);
                }})();
              </script>
            </div>
        '''
        return mark_safe(html)

    location_map.short_description = "Location (Map)"

    class Media:
        js = (
            'turf/location_picker.js',
        )


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
