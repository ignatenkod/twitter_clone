from django.urls import path
from .views import (NotificationListView, mark_notification_as_read, 
                    get_unread_count)

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('<int:pk>/read/', mark_notification_as_read, name='mark_as_read'),
    path('unread_count/', get_unread_count, name='unread_count'),
]
