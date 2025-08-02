from django.urls import path
from .views import (RegistrationView, LoginView, LogoutView, 
                    ProfileView, ProfileUpdateView, toggle_subscription)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('<str:username>/subscribe/', toggle_subscription, name='toggle_subscription'),
]
