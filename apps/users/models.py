from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Кастомная модель пользователя с дополнительными полями"""
    
    bio = models.TextField(
        _('Биография'),
        blank=True,
        null=True,
        help_text=_('Расскажите немного о себе')
    )
    avatar = models.ImageField(
        _('Аватар'),
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text=_('Загрузите ваш аватар')
    )
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})


class Subscription(models.Model):
    """Модель подписки пользователей друг на друга"""
    
    subscriber = models.ForeignKey(
        User,
        verbose_name=_('Подписчик'),
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    subscribed_to = models.ForeignKey(
        User,
        verbose_name=_('Подписка'),
        related_name='subscribers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        _('Дата подписки'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')
        unique_together = ('subscriber', 'subscribed_to')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.subscriber} подписан на {self.subscribed_to}'
    
    def save(self, *args, **kwargs):
        """Проверка, что пользователь не подписывается на себя"""
        if self.subscriber == self.subscribed_to:
            raise ValueError(_('Нельзя подписаться на самого себя'))
        super().save(*args, **kwargs)
