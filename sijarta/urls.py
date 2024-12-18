"""
URL configuration for sijarta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from main import views as main_views  # Import view dari app main


urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('main/', include('main.urls')),
    path('', main_views.landing_page, name='landing_page'),  # Root URL diarahkan ke landing page
    path('', include('main.urls')),
    path('', include('mypay.urls')),
    path('', include('pekerjajasa.urls')),
    path('testimoni/', include('testimoni.urls')),
    path('discount/', include('discount.urls')),

]
