from django.urls import path
from pekerjajasa.views import *

app_name = 'pekerjajasa'

urlpatterns = [
    path('pekerjajasa/', pekerjaan_jasa_view, name='pekerjaan_jasa_view'),
    path('kerjakan-pesanan/<int:pesanan_id>/', kerjakan_pesanan_view, name='kerjakan_pesanan_view'),
    path('statuspekerjaan/', status_pekerjaan_jasa_view, name='status_pekerjaan_jasa_view'),
    path('status/update/<int:pesanan_id>/', update_status_view, name='update_status_view'),
]