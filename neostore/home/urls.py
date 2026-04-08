from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.redirect_to_home),
    path('register/', views.register, name='register'),
]
