from rest_framework import serializers
from .models import PengajuanPenawaranPengadaan

class PengajuanPenawaranPengadaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PengajuanPenawaranPengadaan
        fields = '__all__'
