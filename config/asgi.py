import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

django_application = get_asgi_application()

User = get_user_model()

class WebSocketJWTAuthMiddleware:
    """Middleware для аутентификации WebSocket соединений через JWT"""
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode('utf-8')
        query_params = dict(param.split('=') for param in query_string.split('&') if '=' in param)
        
        token = query_params.get('token', None)
        
        if token:
            try:
                access_token = AccessToken(token)
                user = await self.get_user(access_token.payload.get('user_id'))
                scope['user'] = user
            except (InvalidToken, TokenError, User.DoesNotExist):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)


def JWTAuthMiddlewareStack(app):
    """Обертка для AuthMiddlewareStack с JWT аутентификацией"""
    return WebSocketJWTAuthMiddleware(AuthMiddlewareStack(app))


# Импортируем WebSocket routing из core
from apps.core.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
