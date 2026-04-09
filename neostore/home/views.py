from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from .models import User, Thing, Certificate, Order, Wallet

def home(request):
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
        return HttpResponse("Forbidden", status=403)
    
    pending_certs = Certificate.objects.filter(state=False)
    orders = Order.objects.filter(state=False)
    return render(request, 'home/hr_dashboard.html', {
        'pending_certs': pending_certs,
        'orders': orders
    })

@login_required
def hr_inventory(request):
    if not request.user.is_superuser:
        return HttpResponse("Forbidden", status=403)
    
    things = Thing.objects.all()
    return render(request, 'home/hr_inventory.html', {'things': things})


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


@login_required
def approve_certificate(request, cert_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    if request.method == 'POST':
        cert = get_object_or_404(Certificate, id=cert_id)
        cert.state = True
        cert.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)
