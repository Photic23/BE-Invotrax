from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdukViewSet, KategoriViewSet

router = DefaultRouter()
router.register(r'produk', ProdukViewSet, basename='produk')
router.register(r'kategori', KategoriViewSet, basename='kategori')

urlpatterns = [
    path('', include(router.urls)),
]
