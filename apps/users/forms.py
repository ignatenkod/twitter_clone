from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Имя пользователя'),
            'email': _('Email'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }


class UserUpdateForm(forms.ModelForm):
    """Форма обновления профиля пользователя"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'bio', 'avatar')
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'bio': _('О себе'),
            'avatar': _('Аватар'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
