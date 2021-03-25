from django.urls import include, path

from rest_framework import routers

from .views import MusicViewSet, FingerprintsViewSet

router = routers.DefaultRouter()
router.register(r'music', MusicViewSet)
router.register(r'fingerprints', FingerprintsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]