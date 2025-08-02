from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import User, Subscription
from .forms import RegistrationForm, UserUpdateForm


class RegistrationView(CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        """Автоматический вход после регистрации"""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return response


class LoginView(BaseLoginView):
    """Авторизация пользователя"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Добавление сообщения об успешном входе"""
        response = super().form_valid(form)
        messages.success(self.request, f'Добро пожаловать, {self.request.user.username}!')
        return response


class LogoutView(BaseLogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        """Добавление сообщения об успешном выходе"""
        messages.info(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(DetailView):
    """Профиль пользователя"""
    model = User
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        """Добавление информации о подписке в контекст"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_user = self.get_object()

        if user.is_authenticated and user != profile_user:
            context['is_subscribed'] = Subscription.objects.filter(
                subscriber=user,
                subscribed_to=profile_user
            ).exists()

        # Получаем посты пользователя
        context['posts'] = profile_user.posts.all().order_by('-created_at')
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        """Получаем текущего пользователя"""
        return self.request.user

    def get_success_url(self):
        """Перенаправление на профиль после обновления"""
        messages.success(self.request, 'Профиль успешно обновлен!')
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})


def toggle_subscription(request, username):
    """Переключение подписки на пользователя"""
    if not request.user.is_authenticated:
        return redirect('users:login')

    subscribed_to = get_object_or_404(User, username=username)
    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        subscribed_to=subscribed_to
    )

    if not created:
        subscription.delete()
        messages.info(request, f'Вы отписались от {username}')
    else:
        messages.success(request, f'Вы подписались на {username}')

    return redirect('users:profile', username=username)
