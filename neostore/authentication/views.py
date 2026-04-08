from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from home.models import Wallet

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            wallet = Wallet.objects.create()
            user.wallet = wallet
            user.save()

            login(request, user)

            return redirect('user-profile')
        else:
            messages.error(request, 'Данные заполнены неверно!')


    data = {
        'form': CustomUserCreationForm()
    }


    return render(request, 'registration/register.html', {'form': data['form'] })
