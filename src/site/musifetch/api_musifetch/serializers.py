from rest_framework import serializers

from .models import Music, Fingerprints


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('__all__')


class FingerprintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprints
        fields = ('hashe', 'id_music')
