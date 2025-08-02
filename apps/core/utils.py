from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

User = get_user_model()

def send_notification_to_user(user_id, notification_data):
    """
    Отправка уведомления конкретному пользователю через WebSocket
    :param user_id: ID пользователя-получателя
    :param notification_data: Данные уведомления (словарь)
    """
    channel_layer = get_channel_layer()
    group_name = f'notifications_{user_id}'
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'notification': notification_data
        }
    )

def update_user_notification_count(user_id):
    """
    Обновление счетчика уведомлений для пользователя
    :param user_id: ID пользователя
    """
    channel_layer = get_channel_layer()
    group_name = f'notifications_{user_id}'
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'update_unread_count',
            'user_id': user_id
        }
    )
