from rest_framework import serializers
from .models import Produk, Kategori
from main.models import CustomUser

class ProdukSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='vendor')
    )

    class Meta:
        model = Produk
        fields = '__all__'

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'