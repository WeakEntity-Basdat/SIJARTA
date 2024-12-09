from django.urls import path
from discount.views import discount_page, purchase_voucher

app_name = 'discount'

urlpatterns = [
    path('', discount_page, name='discount_page'),
    path('purchase/<str:voucher_id>/', purchase_voucher, name='purchase_voucher'),
]
