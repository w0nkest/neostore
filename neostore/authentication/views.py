from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from home.models import Wallet, Cart

def register(request):
    error = ''
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
            error = 'Данные заполнены неверно!'


    data = {
        'form': CustomUserCreationForm(),
        'error': error
    }


    return render(request, 'registration/register.html', data)


def custom_logout(request):
    if request.user.is_authenticated:
        # получаем корзину пользователя
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            # возвращаем товары на склад
            for item in cart.items.all():
                item.thing.amount += item.quantity
                item.thing.save()
            # удаляем корзину
            cart.delete()

    logout(request)
    return redirect('home')