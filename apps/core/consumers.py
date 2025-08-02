import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    """Consumer для уведомлений в реальном времени"""
    
    async def connect(self):
        """Обработка подключения WebSocket"""
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.user_group_name = f'notifications_{self.scope["user"].id}'
            
            # Присоединяемся к группе уведомлений пользователя
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            
            await self.accept()
    
    async def disconnect(self, close_code):
        """Обработка отключения WebSocket"""
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def send_notification(self, event):
        """Отправка уведомления клиенту"""
        notification = event['notification']
        
        # Отправляем уведомление через WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
    
    @database_sync_to_async
    def get_unread_count(self, user_id):
        """Получение количества непрочитанных уведомлений"""
        return Notification.objects.filter(recipient_id=user_id, is_read=False).count()
    
    async def receive(self, text_data):
        """Обработка входящих сообщений"""
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'get_unread_count':
            # Отправляем количество непрочитанных уведомлений
            count = await self.get_unread_count(self.scope['user'].id)
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': count
            }))
