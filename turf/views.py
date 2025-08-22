from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Turf, PitchType, GameTime, Purpose, Facility
from .serializers import (
    TurfSerializer,
    TurfListSerializer,
    PitchTypeSerializer,
    GameTimeSerializer,
    PurposeSerializer,
    FacilitySerializer
)
from .filters import TurfFilter



class TurfViewSet(viewsets.ModelViewSet):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TurfFilter
    def get_serializer_class(self):
        if self.action == "list":
            return TurfListSerializer
        return TurfSerializer


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
