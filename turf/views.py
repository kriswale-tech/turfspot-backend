from rest_framework import viewsets
from rest_framework.filters import SearchFilter
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
from rest_framework.views import APIView
from rest_framework.response import Response
import math


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class NearestTurfsView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get('lat'))
            user_lon = float(request.query_params.get('lon'))
        except (TypeError, ValueError):
            return Response({'error': 'lat and lon query parameters are required and must be valid numbers.'}, status=400)
        turfs = Turf.objects.all()
        turfs_with_distance = []
        for turf in turfs:
            if turf.latitude is not None and turf.longitude is not None:
                distance = haversine(user_lat, user_lon, turf.latitude, turf.longitude)
                turfs_with_distance.append({
                    'turf': turf,
                    'distance': distance
                })
        turfs_with_distance.sort(key=lambda x: x['distance'])
        data = [
            dict(TurfListSerializer(t['turf']).data, distance=t['distance'])
            for t in turfs_with_distance
        ]
        return Response(data)


class TurfViewSet(viewsets.ModelViewSet):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TurfFilter
    search_fields = ["name", "location"]
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
