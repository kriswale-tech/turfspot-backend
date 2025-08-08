from rest_framework import viewsets
from .models import TurfSpot
from .serializers import TurfSpotSerializer
from rest_framework.permissions import AllowAny

class TurfSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TurfSpot.objects.all()
    serializer_class = TurfSpotSerializer
    permission_classes = [AllowAny]
