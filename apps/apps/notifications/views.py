from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    """Список уведомлений пользователя"""
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        """Получаем только уведомления текущего пользователя"""
        return Notification.objects.filter(recipient=self.request.user)\
            .select_related('sender', 'post')\
            .order_by('-created_at')


def mark_notification_as_read(request, pk):
    """Пометить уведомление как прочитанное"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Требуется авторизация'}, status=401)

    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    
    return JsonResponse({'status': 'success'})


def get_unread_count(request):
    """Получить количество непрочитанных уведомлений"""
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})

    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})
