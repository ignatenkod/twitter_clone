from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Post(models.Model):
    """Модель поста в микроблоге"""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Автор'),
        related_name='posts',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        _('Содержание'),
        max_length=500,
        help_text=_('Максимальная длина поста 500 символов')
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='posts/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Пост #{self.id} от {self.author.username}'
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})
    
    @property
    def likes_count(self):
        """Количество лайков у поста"""
        return self.likes.count()
    
    @property
    def comments_count(self):
        """Количество комментариев у поста"""
        return self.comments.count()


class Like(models.Model):
    """Модель лайка к посту"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        related_name='likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        verbose_name=_('Пост'),
        related_name='likes',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Лайк')
        verbose_name_plural = _('Лайки')
        unique_together = ('user', 'post')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Лайк от {self.user.username} к посту #{self.post.id}'


class Comment(models.Model):
    """Модель комментария к посту"""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Автор'),
        related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        verbose_name=_('Пост'),
        related_name='comments',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        _('Содержание'),
        max_length=300
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к посту #{self.post.id}'
