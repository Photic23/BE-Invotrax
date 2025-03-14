from django.db import models
from django.contrib.auth.models import User

class PenawaranPengadaan(models.Model):
    # supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    nama_produk = models.CharField(max_length=255)
    # kategori_produk = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    jumlah_produk = models.PositiveIntegerField()
    deskripsi_produk = models.TextField(blank=True, null=True)
    url_foto_produk = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)