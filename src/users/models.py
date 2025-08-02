from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Модель пользователя с дополнительными полями.
    Наследуется от AbstractUser для стандартной аутентификации.
    """
    bio = models.TextField(_('Биография'), blank=True)
    avatar = models.ImageField(
        _('Аватар'), 
        upload_to='avatars/', 
        blank=True, 
        null=True
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        verbose_name=_('Подписчики')
    )
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})
    
    def follow(self, user):
        """Подписаться на пользователя"""
        self.following.add(user)
    
    def unfollow(self, user):
        """Отписаться от пользователя"""
        self.following.remove(user)
    
    def is_following(self, user):
        """Проверка, подписан ли текущий пользователь на другого"""
        return self.following.filter(pk=user.pk).exists()
    
    @property
    def followers_count(self):
        """Количество подписчиков"""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Количество подписок"""
        return self.following.count()


class UserProfile(models.Model):
    """
    Дополнительный профиль пользователя с настройками.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Пользователь')
    )
    email_notifications = models.BooleanField(
        _('Email уведомления'),
        default=True,
        help_text=_('Получать уведомления на email')
    )
    push_notifications = models.BooleanField(
        _('Push уведомления'),
        default=True,
        help_text=_('Получать push уведомления в браузере')
    )
    
    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
    
    def __str__(self):
        return f'Профиль {self.user.username}'
