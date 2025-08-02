import os
from django.core.asgi import get_asgi_application
from config.routing import application as websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

django_application = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] == 'http':
        await django_application(scope, receive, send)
    else:
        await websocket_application(scope, receive, send)
