from django.urls import path
from . import views

urlpatterns = [
    path('discount/', views.discount_page, name='discount_page'),
    path('purchase/<int:voucher_id>/', views.purchase_voucher, name='purchase_voucher'),
]
