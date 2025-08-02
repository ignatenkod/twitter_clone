import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer для обработки уведомлений в реальном времени"""
    
    async def connect(self):
        """Обработка подключения пользователя"""
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.notification_group_name = f'notifications_{self.user.id}'
            
            # Присоединяемся к группе уведомлений
            await self.channel_layer.group_add(
                self.notification_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Отправляем текущее количество непрочитанных уведомлений
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))

    async def disconnect(self, close_code):
        """Обработка отключения пользователя"""
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """Обработка входящих сообщений"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_as_read':
                # Пометить уведомление как прочитанное
                notification_id = data.get('notification_id')
                if notification_id:
                    await self.mark_notification_as_read(notification_id)
                    unread_count = await self.get_unread_count()
                    await self.send(text_data=json.dumps({
                        'type': 'unread_count',
                        'count': unread_count
                    }))
            
            elif message_type == 'get_unread_count':
                # Запрос количества непрочитанных уведомлений
                unread_count = await self.get_unread_count()
                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'count': unread_count
                }))
                
        except json.JSONDecodeError:
            pass

    async def send_notification(self, event):
        """Отправка уведомления клиенту"""
        notification = event['notification']
        unread_count = await self.get_unread_count()
        
        # Отправляем как само уведомление, так и обновленный счетчик
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification,
            'unread_count': unread_count
        }))

    @database_sync_to_async
    def get_unread_count(self):
        """Получение количества непрочитанных уведомлений"""
        return Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).count()

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """Пометить уведомление как прочитанное"""
        Notification.objects.filter(
            id=notification_id,
            recipient=self.user
        ).update(is_read=True)
