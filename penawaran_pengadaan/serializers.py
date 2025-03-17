from rest_framework import serializers
from .models import PenawaranPengadaan

class PenawaranPengadaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenawaranPengadaan
        fields = '__all__'