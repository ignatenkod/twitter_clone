from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count

from .models import Post, Like, Comment
from .forms import PostCreateForm, CommentCreateForm
from apps.notifications.models import Notification


class FeedView(LoginRequiredMixin, ListView):
    """Лента постов пользователей, на которых подписан текущий пользователь"""
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Получаем посты пользователей, на которых подписан текущий пользователь"""
        subscribed_to = self.request.user.subscriptions.values_list('subscribed_to', flat=True)
        return Post.objects.filter(author_id__in=subscribed_to)\
            .annotate(comments_count=Count('comments'))\
            .order_by('-created_at')\
            .select_related('author')


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание нового поста"""
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        """Установка автора поста перед сохранением"""
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Пост успешно создан!')
        return response


class PostDetailView(DetailView):
    """Детальная страница поста"""
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Добавление формы комментария и списка комментариев в контекст"""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm()
        context['comments'] = self.object.comments.select_related('author').order_by('-created_at')
        
        if self.request.user.is_authenticated:
            context['is_liked'] = self.object.likes.filter(user=self.request.user).exists()
        
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление поста"""
    model = Post
    success_url = reverse_lazy('posts:feed')

    def get_queryset(self):
        """Ограничиваем удаление только своими постами"""
        return super().get_queryset().filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Добавление сообщения об успешном удалении"""
        messages.success(request, 'Пост успешно удален!')
        return super().delete(request, *args, **kwargs)


def toggle_like(request, pk):
    """Переключение лайка поста"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)

    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    likes_count = post.likes.count()
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': likes_count
    })


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария"""
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        """Установка автора и поста перед сохранением"""
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        response = super().form_valid(form)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'author': self.request.user.username,
                    'content': form.instance.content,
                    'created_at': form.instance.created_at.strftime('%d.%m.%Y %H:%M'),
                    'avatar_url': self.request.user.avatar.url if self.request.user.avatar else ''
                }
            })
        
        return response

    def get_success_url(self):
        """Перенаправление на страницу поста после успешного создания комментария"""
        return reverse_lazy('posts:detail', kwargs={'pk': self.kwargs['pk']})
