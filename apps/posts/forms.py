from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    """Форма создания поста"""
    
    class Meta:
        model = Post
        fields = ('content', 'image')
        labels = {
            'content': _('Содержание'),
            'image': _('Изображение'),
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('Что у вас нового?')
            }),
        }


class CommentCreateForm(forms.ModelForm):
    """Форма создания комментария"""
    
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': _('Комментарий'),
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': _('Напишите комментарий...')
            }),
        }
