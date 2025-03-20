from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PenawaranPengadaanViewSet

router = DefaultRouter()
router.register(r'penawaran-pengadaan', PenawaranPengadaanViewSet, basename='penawaranpengadaan')

urlpatterns = [
    path('', include(router.urls)),
]
