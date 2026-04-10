from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('dashboard/', views.employee_dashboard, name='employee-dashboard'),
    path('hr/dashboard/', views.hr_dashboard, name='hr-dashboard'),
    path('hr/challenges', views.challenge, name='challenge'),
    path('mark-order/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),
    path('approve-cert/<int:cert_id>/', views.approve_certificate, name='approve_certificate'),
    path('delete-cert/<int:cert_id>/', views.delete_certificate, name='delete_certificate'),
    path('hr/wallet/creation', views.wallet_creation, name='wallet-creation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
