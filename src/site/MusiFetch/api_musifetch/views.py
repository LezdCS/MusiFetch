from rest_framework import viewsets

from .serializers import MusicSerializer, FingerprintsSerializer
from .models import Music, Fingerprints
from rest_framework.response import Response


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class FingerprintsViewSet(viewsets.ModelViewSet):
    queryset = Fingerprints.objects.all()
    serializer_class = FingerprintsSerializer
