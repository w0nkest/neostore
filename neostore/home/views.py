from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from .models import User


def home(request):
    users = User.objects.all()
    return render(request, 'home/home.html', {'users': users})


class UserProfileView(LoginRequiredMixin, DetailView):
    """Просмотр своего профиля без указания ID"""
    model = get_user_model()
    context_object_name = 'user'
    template_name = 'home/user_detail.html'

    def get_object(self):
        return self.request.user