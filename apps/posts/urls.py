from django.urls import path
from .views import (FeedView, PostCreateView, PostDetailView, 
                    PostDeleteView, toggle_like, CommentCreateView)

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/like/', toggle_like, name='toggle_like'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
]
