from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('register/register_pengguna/', registrasi_pengguna, name='register_pengguna'),
    path('register/register_pekerja/', registrasi_pekerja, name='register_pekerja'),
    path('profile/pekerja/', profile_pekerja, name='profile_pekerja'),
    path('profile/pengguna/', profile, name='profile_pengguna'),

]