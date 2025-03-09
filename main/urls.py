from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Your other URLs
    path('test-db-connection/', views.test_db_connection, name='test_db_connection'),
]