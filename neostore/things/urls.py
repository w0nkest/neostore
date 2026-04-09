from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.display, name='store'),
    path('add/', views.add, name='add-things'),
    path('cart/', views.cart_display, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart-ajax/<int:thing_id>/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('get-cart-item/<int:thing_id>/', views.get_cart_item, name='get_cart_item'),
    path('update-cart-quantity/<int:thing_id>/', views.update_cart_quantity, name='update_cart_quantity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
