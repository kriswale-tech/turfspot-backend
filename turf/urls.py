from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurfSpotViewSet

router = DefaultRouter()
router.register(r'turfs', TurfSpotViewSet, basename='turf')

urlpatterns = [
    path('', include(router.urls)),
]
