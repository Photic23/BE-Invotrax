from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be_invotrax.settings")  # Adjust if your settings module is different

app = get_wsgi_application()