from rest_framework import viewsets
from .models import TurfSpot, PitchType, GameTime, Purpose, Facility
from .serializers import (
    TurfSpotSerializer,
    PitchTypeSerializer,
    GameTimeSerializer,
    PurposeSerializer,
    FacilitySerializer
)


class TurfSpotViewSet(viewsets.ModelViewSet):
    queryset = TurfSpot.objects.all()
    serializer_class = TurfSpotSerializer


class PitchTypeViewSet(viewsets.ModelViewSet):
    queryset = PitchType.objects.all()
    serializer_class = PitchTypeSerializer


class GameTimeViewSet(viewsets.ModelViewSet):
    queryset = GameTime.objects.all()
    serializer_class = GameTimeSerializer


class PurposeViewSet(viewsets.ModelViewSet):
    queryset = Purpose.objects.all()
    serializer_class = PurposeSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
