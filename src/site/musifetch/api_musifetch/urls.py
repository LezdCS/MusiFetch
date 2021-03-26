from django.urls import include, path


from .views import MusicViewSet, FingerprintsViewSet


urlpatterns = [
    path(r'music', MusicViewSet.as_view(), name='music'),
    path(r'fingerprints', FingerprintsViewSet.as_view(), name='fingerprints'),
]