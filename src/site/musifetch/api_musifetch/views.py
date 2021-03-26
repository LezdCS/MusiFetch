from rest_framework import viewsets
from .serializers import MusicSerializer, FingerprintsSerializer
from .models import Music, Fingerprints

from rest_framework.views import APIView
from rest_framework.response import Response

import sys

sys.path.append("..")  # Adds higher directory to python modules path.
from fingerprints import fingerprints_generator


class MusicViewSet(APIView):
    def get(self, request, *args, **kwargs):
        qs = Music.objects.all()
        serializer = MusicSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *arqs, **kwargs):
        algo = fingerprints_generator.Algo()
        algo.choice("create", request.data['url'])

        return Response("Successfuly created")


class FingerprintsViewSet(APIView):

    def post(self, request, *args, **kwargs):
        algo = fingerprints_generator.Algo()
        algo.choice("find", request.data['url'])

        return Response(algo.occurences)
