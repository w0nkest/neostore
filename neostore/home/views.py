from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from .models import User, Thing, Certificate, Order, Wallet

User = get_user_model()

def home(request):
    return render(request, 'home/home.html')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'home/user_detail.html'

    def get_object(self):
        return self.request.user

@login_required
def employee_dashboard(request):
    user = request.user
    balance = user.wallet.money if user.wallet else 0
    my_certificates = Certificate.objects.filter(user=user)
    return render(request, 'home/employee_dashboard.html', {
        'balance': balance,
        'certificates': my_certificates
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
