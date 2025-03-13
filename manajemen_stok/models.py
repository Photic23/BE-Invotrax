from django.db import models
from django.contrib.auth.models import User

class Kategori(models.Model):
    nama = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nama
    
class Produk(models.Model):
    nama = models.CharField(max_length=255)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    #supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    #kontrak = models.ForeignKey(Kontrak, on_delete=models.SET_NULL, null=True)
    stok = models.PositiveIntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    harga = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nama