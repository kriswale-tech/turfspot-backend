from django.contrib import admin
from .models import Turf, PitchType, GameTime, Purpose, Facility, TurfImage, WhatsappNumber, CallNumber
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class TurfImageAdminForm(forms.ModelForm):
    class Meta:
        model = TurfImage
        fields = "__all__"
        help_texts = {
            "image": "Images are optimized automatically on delivery",
        }

    def clean_image(self):
        img_file = self.cleaned_data.get("image")
        if not img_file:
            return img_file
        try:
            try:
                img_file.seek(0)
            except Exception:
                pass
            img = Image.open(img_file)
            img_format = (img.format or 'JPEG').upper()
            if img_format not in ("JPEG", "JPG", "PNG", "WEBP"):
                img_format = "JPEG"
            if img.mode in ("RGBA", "P") and img_format in ("JPEG", "JPG"):
                img = img.convert("RGB")
            # Resize to reasonable width for admin uploads
            max_width = 2000
            w, h = img.size
            if w > max_width:
                ratio = max_width / float(w)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
            # Compress to fit under ~10MB
            max_bytes = 10 * 1024 * 1024
            quality = 85
            min_quality = 60
            buf = BytesIO()
            img.save(buf, format="JPEG" if img_format in ("JPEG", "JPG") else img_format, optimize=True, quality=quality)
            while buf.tell() > max_bytes and quality > min_quality:
                quality -= 5
                buf.seek(0)
                buf.truncate()
                img.save(buf, format="JPEG" if img_format in ("JPEG", "JPG") else img_format, optimize=True, quality=quality)
            buf.seek(0)
            filename = getattr(img_file, 'name', f'upload.{img_format.lower()}')
            content_type = 'image/jpeg' if img_format in ("JPEG", "JPG") else f'image/{img_format.lower()}'
            return InMemoryUploadedFile(
                buf,
                field_name=None,
                name=filename,
                content_type=content_type,
                size=buf.getbuffer().nbytes,
                charset=None
            )
        except Exception:
            # If compression fails, return original to avoid blocking admin
            return img_file


class TurfImageInline(admin.StackedInline):  # use StackedInline to show help_text
    model = TurfImage
    extra = 1
    form = TurfImageAdminForm


def _split_numbers(raw: str):
    if not raw:
        return []
    # split by comma or newline and strip
    parts = [p.strip() for p in raw.replace("\r", "").replace(",", "\n").split("\n")]
    return [p for p in parts if p]


class TurfAdminForm(forms.ModelForm):
    whatsapp_numbers_text = forms.CharField(
        required=False,
        label="WhatsApp numbers",
        help_text="Enter numbers separated by comma or new lines",
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    call_numbers_text = forms.CharField(
        required=False,
        label="Call numbers",
        help_text="Enter numbers separated by comma or new lines",
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    class Meta:
        model = Turf
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["whatsapp_numbers_text"].initial = "\n".join(
                instance.whatsapp_numbers.values_list("number", flat=True)
            )
            self.fields["call_numbers_text"].initial = "\n".join(
                instance.call_numbers.values_list("number", flat=True)
            )

@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    form = TurfAdminForm
    list_display = ("name", "pitch_type", "price_per_hour", "location", "latitude", "longitude", "created_at")
    inlines = [TurfImageInline]
    exclude = ("whatsapp_numbers", "call_numbers")

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
                "location",
                "whatsapp_numbers_text",
                "call_numbers_text",
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Save WhatsApp numbers
        wa_numbers = [_ for _ in _split_numbers(form.cleaned_data.get("whatsapp_numbers_text", ""))]
        if wa_numbers is not None:
            wa_objs = [WhatsappNumber.objects.get_or_create(number=n)[0] for n in wa_numbers]
            obj.whatsapp_numbers.set(wa_objs)
        # Save Call numbers
        call_numbers = [_ for _ in _split_numbers(form.cleaned_data.get("call_numbers_text", ""))]
        if call_numbers is not None:
            call_objs = [CallNumber.objects.get_or_create(number=n)[0] for n in call_numbers]
            obj.call_numbers.set(call_objs)


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
