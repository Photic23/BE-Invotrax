import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "be_invotrax.settings")

app = get_asgi_application()  # ASGI application for Vercel
