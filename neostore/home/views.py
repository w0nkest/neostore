from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from .models import User, Thing, Certificate, Order, Wallet
# from neostore.junk_catch import cleanup


def home(request):
    # cleanup()
    return render(request, 'home/home.html')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'home/user_detail.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["pending_certs"] = Certificate.objects.filter(user=user, state=False).count()
        context['active_orders'] = Order.objects.filter(user=user, state=False).count()

        return context


@login_required
def employee_dashboard(request):
    user = request.user
    balance = user.wallet.money if user.wallet else 0
    my_certificates = Certificate.objects.filter(user=user)
    my_orders = Order.objects.filter(user=user)
    return render(request, 'home/employee_dashboard.html', {
        'balance': balance,
        'certificates': my_certificates,
        'orders': my_orders,
    })


@login_required
def store(request):
    things = Thing.objects.filter(amount__gt=0)
    return render(request, 'home/store.html', {'things': things})


@login_required
def hr_dashboard(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    pending_certs = Certificate.objects.filter(state=False)
    approved_certs = Certificate.objects.filter(state=True)
    orders = Order.objects.filter(state=False)
    return render(request, 'home/hr_dashboard.html', {
        'pending_certs': pending_certs,
        'approved_certs': approved_certs,
        'orders': orders
    })


@login_required
def mark_order_delivered(request, order_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.state = True
        order.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)


import json


@login_required
def approve_certificate(request, cert_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        reward = data.get('reward', 0)

        if reward <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid reward amount'}, status=400)

        cert = get_object_or_404(Certificate, id=cert_id)
        cert.state = True
        cert.save()

        wallet = cert.user.wallet
        wallet.money += reward
        wallet.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)


@login_required
def challenge(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    if request.method == 'POST':
        selected_users_json = request.POST.get('selected_users')
        amount = int(request.POST.get('amount', 0))

        if amount <= 0:
            messages.error(request, 'Invalid amount')
            return redirect('challenge')

        selected_users = json.loads(selected_users_json)

        for user_id in selected_users:
            user = User.objects.get(id=user_id)
            user.wallet.money += amount
            user.wallet.save()

        messages.success(request, f'Successfully rewarded {amount} NeoCoins to {len(selected_users)} user(s)')
        return redirect('challenge')

    users = User.objects.all()
    nowallet = any(user.wallet is None for user in users)

    return render(request, 'home/challenges.html', {'users': users, 'nowallet': nowallet})


@login_required
def delete_certificate(request, cert_id):
    if request.method == 'POST':
        cert = get_object_or_404(Certificate, id=cert_id, user=request.user)
        if cert.state:
            return JsonResponse({'success': False, 'error': 'Нельзя удалить одобренный сертификат'}, status=400)
        cert.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неверный метод'}, status=400)


@login_required
def wallet_creation(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    users = User.objects.all()
    for user in users:
        if user.wallet is None:
            wallet = Wallet.objects.create()
            user.wallet = wallet
            user.save()

    return redirect('challenge')
