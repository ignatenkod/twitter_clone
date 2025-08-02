from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Notification(models.Model):
    """Модель уведомления для пользователя"""
    
    class NotificationType(models.TextChoices):
        NEW_POST = 'new_post', _('Новый пост')
        NEW_LIKE = 'new_like', _('Новый лайк')
        NEW_COMMENT = 'new_comment', _('Новый комментарий')
        NEW_SUBSCRIBER = 'new_subscriber', _('Новый подписчик')
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Получатель'),
        related_name='notifications',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Отправитель'),
        related_name='sent_notifications',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    notification_type = models.CharField(
        _('Тип уведомления'),
        max_length=20,
        choices=NotificationType.choices
    )
    message = models.CharField(
        _('Сообщение'),
        max_length=255
    )
    post = models.ForeignKey(
        'posts.Post',
        verbose_name=_('Пост'),
        related_name='notifications',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_read = models.BooleanField(
        _('Прочитано'),
        default=False
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Уведомление для {self.recipient.username}: {self.message}'
    
    def mark_as_read(self):
        """Пометить уведомление как прочитанное"""
        self.is_read = True
        self.save()
