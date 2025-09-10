import django_filters
from .models import Turf, PitchType, Purpose, Facility


class TurfFilter(django_filters.FilterSet):
    # Sorting: Alphabetical, Location, Cheapest
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('location', 'location'),
            ('price_per_hour', 'price_per_hour'),
        ),
        field_labels={
            'name': 'Alphabetical',
            'location': 'Location',
            'price_per_hour': 'Cost',
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

    # Purposes (M2M, allow multiple)
    purposes = django_filters.ModelMultipleChoiceFilter(
        field_name="purposes",
        queryset=Purpose.objects.all(),
        label="Purposes"
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
            "purposes",
            "facilities",
        ]
