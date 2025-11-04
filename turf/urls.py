from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TurfViewSet,
    PitchTypeViewSet,
    GameTimeViewSet,
    PurposeViewSet,
    FacilityViewSet,
    NearestTurfsView,
    SuggestTurfsView,
)

router = DefaultRouter()
router.register(r'turfs', TurfViewSet)
router.register(r'pitchtypes', PitchTypeViewSet)
router.register(r'gametimes', GameTimeViewSet)
router.register(r'purposes', PurposeViewSet)
router.register(r'facilities', FacilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('turfs/nearest/', NearestTurfsView.as_view(), name='nearest-turfs'),
    path('turfs/suggest/', SuggestTurfsView.as_view(), name='suggest-turfs'),
]
