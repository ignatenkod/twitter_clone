from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import Post


@shared_task
def send_new_post_email(post_id, recipient_list):
    """
    Отправка email-уведомлений о новом посте
    :param post_id: ID поста
    :param recipient_list: Список email получателей
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return
    
    subject = _('Новый пост от {}').format(post.author.username)
    
    # Рендеринг HTML сообщения
    message = render_to_string('emails/new_post.html', {
        'post': post,
        'site_url': settings.SITE_URL
    })
    
    send_mail(
        subject=subject,
        message='',
        html_message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True
    )
