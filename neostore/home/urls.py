from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('dashboard/', views.employee_dashboard, name='employee-dashboard'),
    path('hr/dashboard/', views.hr_dashboard, name='hr-dashboard'),
    path('hr/inventory/', views.hr_inventory, name='hr-inventory'),
    path('mark-order/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),
    path('approve-cert/<int:cert_id>/', views.approve_certificate, name='approve_certificate'),
]
