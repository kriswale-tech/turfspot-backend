import django_filters
from .models import Turf, PitchType, GameTime, Purpose, Facility


class TurfFilter(django_filters.FilterSet):
    # Sorting: Cheapest
    ordering = django_filters.OrderingFilter(
        fields=(
            ('price_per_hour', 'price_per_hour'),
        ),
        field_labels={
            'price_per_hour': 'Cheapest',
        },
        label='Sort',
    )

    # Pitch Type (FK)
    pitch_type = django_filters.ModelChoiceFilter(
        queryset=PitchType.objects.all(),
        label="Pitch Type"
    )

    # Price per hour (range filter)
    price_per_hour = django_filters.RangeFilter(label="Price Per Hour")

    # Game Time (FK)
    game_time = django_filters.ModelChoiceFilter(
        queryset=GameTime.objects.all(),
        label="Game Time"
    )

    # Purpose (FK)
    purpose = django_filters.ModelChoiceFilter(
        queryset=Purpose.objects.all(),
        label="Purpose"
    )

    # Facilities (M2M, allow multiple)
    facilities = django_filters.ModelMultipleChoiceFilter(
        field_name="facilities",
        queryset=Facility.objects.all(),
        label="Facilities"
    )

    class Meta:
        model = Turf
        fields = [
            "pitch_type",
            "price_per_hour",
            "game_time",
            "purpose",
            "facilities",
        ]
