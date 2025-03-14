from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Produk, Kategori
from .serializers import ProdukSerializer, KategoriSerializer

class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.filter(is_deleted=False)
    serializer_class = ProdukSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def daftar_produk(self, request):
        produk_list = self.get_queryset()
        serializer = self.get_serializer(produk_list, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.AllowAny])
    def update_produk(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        serializer = self.get_serializer(produk, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def detail_produk(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        serializer = self.get_serializer(produk)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.AllowAny])
    def hapus_produk(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        produk.is_deleted = True
        produk.save()
        return Response({"message": "Produk berhasil dihapus (soft delete)"}, status=200)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.AllowAny])
    def update_stok(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        stok_baru = request.data.get("stok")
        if stok_baru is not None:
            try:
                stok_baru = int(stok_baru)
                if stok_baru < 0:
                    return Response({"error": "Stok tidak boleh negatif"}, status=400)
                produk.stok = stok_baru
                produk.save()
                return Response({"message": "Stok berhasil diperbarui", "stok": produk.stok})
            except ValueError:
                return Response({"error": "Stok harus berupa angka"}, status=400)
        return Response({"error": "Field 'stok' harus disertakan"}, status=400)

class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.filter(is_deleted=False)
    serializer_class = KategoriSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'], permission_classes=[permissions.AllowAny])
    def update_kategori(self, request, pk=None):
        kategori = get_object_or_404(Kategori, pk=pk, is_deleted=False)
        serializer = self.get_serializer(kategori, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def daftar_kategori(self, request):
        kategori_list = self.get_queryset()
        serializer = self.get_serializer(kategori_list, many=True)
        return Response(serializer.data)