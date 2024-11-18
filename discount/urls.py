from django.urls import path
from . import views

urlpatterns = [
    path('discount/', views.discount_page, name='discount_page'),
    path('purchase/1/', views.purchase_voucher, name='purchase_voucher'),
]
