from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.posts.models import Like, Comment
from apps.users.models import Subscription
from .models import Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Создание уведомления о новом лайке"""
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type=Notification.NotificationType.NEW_LIKE,
            message=_('{user} поставил лайк вашему посту').format(user=instance.user.username),
            post=instance.post
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Создание уведомления о новом комментарии"""
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.author,
            notification_type=Notification.NotificationType.NEW_COMMENT,
            message=_('{user} оставил комментарий к вашему посту').format(user=instance.author.username),
            post=instance.post
        )


@receiver(post_save, sender=Subscription)
def create_subscription_notification(sender, instance, created, **kwargs):
    """Создание уведомления о новой подписке"""
    if created:
        Notification.objects.create(
            recipient=instance.subscribed_to,
            sender=instance.subscriber,
            notification_type=Notification.NotificationType.NEW_SUBSCRIBER,
            message=_('{user} подписался на вас').format(user=instance.subscriber.username)
        )
