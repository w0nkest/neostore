from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('dashboard/', views.employee_dashboard, name='employee-dashboard'),
    path('store/', views.store, name='store'),
    path('hr/dashboard/', views.hr_dashboard, name='hr-dashboard'),
    path('hr/inventory/', views.hr_inventory, name='hr-inventory'),
]
