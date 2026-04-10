from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', form_class=CustomAuthenticationForm), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
]
