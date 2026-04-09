import json
import os
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ThingsForm
from home.models import Thing, Cart, CartItem


def display(request):
    things = Thing.objects.all()
    return render(request, 'things/store.html', {'things': things})


def add(request):
    error = ''
    if request.method == 'POST':
        form = ThingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')
        else:
            print(form.errors)
            print()
            print(form)
            error = 'Данные не верны!'

    form = ThingsForm()
    data = {'form': form, 'error': error}
    return render(request, 'things/adder.html', data)


@login_required
def add_to_cart_ajax(request, thing_id):
    if request.method == 'POST':
        thing = get_object_or_404(Thing, id=thing_id)

        if thing.amount <= 0:
            return JsonResponse({
                'success': False,
                'error': 'Out of stock!'
            }, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, thing=thing)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        thing.amount -= 1
        thing.save()

        total_items = sum(item.quantity for item in cart.items.all())

        return JsonResponse({
            'success': True,
            'cart_count': total_items,
            'new_stock': thing.amount
        })

    return JsonResponse({'success': False}, status=400)


@login_required
def cart_count(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    total_items = sum(item.quantity for item in cart.items.all())
    return JsonResponse({'cart_count': total_items})


@login_required
def get_cart_item(request, thing_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, thing_id=thing_id).first()
    thing = get_object_or_404(Thing, id=thing_id)
    quantity = cart_item.quantity if cart_item else 0
    return JsonResponse({
        'quantity': quantity,
        'stock': thing.amount
    })


@login_required
def update_cart_quantity(request, thing_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_quantity = data.get('quantity', 0)
        thing = get_object_or_404(Thing, id=thing_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        old_item = CartItem.objects.filter(cart=cart, thing=thing).first()
        old_quantity = old_item.quantity if old_item else 0

        if new_quantity > old_quantity:
            diff_to_add = new_quantity - old_quantity
            if diff_to_add > thing.amount:
                return JsonResponse({
                    'success': False,
                    'error': f'Only {thing.amount} left',
                    'max_reached': True,
                    'stock': thing.amount
                }, status=400)

        diff = old_quantity - new_quantity

        if new_quantity <= 0:
            CartItem.objects.filter(cart=cart, thing=thing).delete()
        else:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, thing=thing)
            cart_item.quantity = new_quantity
            cart_item.save()

        thing.amount += diff
        thing.save()

        total_items = sum(item.quantity for item in cart.items.all())
        cart_total = sum(item.thing.value * item.quantity for item in cart.items.all())

        return JsonResponse({
            'success': True,
            'quantity': new_quantity,
            'cart_count': total_items,
            'cart_total': cart_total,
            'stock': thing.amount
        })

    return JsonResponse({'success': False}, status=400)



@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    totalprice = sum(it.subtotal for it in items)

    return render(request, 'things/cart.html', {'items': items, 'totalprice': totalprice})
