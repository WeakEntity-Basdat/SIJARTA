from django.urls import path
from mypay.views import *

app_name = 'mypay'

urlpatterns = [
    path('mypay/', mypay_view, name='mypay_view'),
    path('transaksi-mypay/', transaksi_mypay_view, name='transaksi_mypay_view'),
    path(' ', proses_transaksi_mypay, name='proses_transaksi_mypay')
   
]
