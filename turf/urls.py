from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TurfSpotViewSet,
    PitchTypeViewSet,
    GameTimeViewSet,
    PurposeViewSet,
    FacilityViewSet
)

router = DefaultRouter()
router.register(r'turfspots', TurfSpotViewSet)
router.register(r'pitchtypes', PitchTypeViewSet)
router.register(r'gametimes', GameTimeViewSet)
router.register(r'purposes', PurposeViewSet)
router.register(r'facilities', FacilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
