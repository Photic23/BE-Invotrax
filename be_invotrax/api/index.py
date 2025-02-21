from be_invotrax.wsgi import application  # Import Django's WSGI application

# Vercel expects a `handler` function
def handler(event, context):
    return application(event, context)