from django.urls import path, include

from main.views import landing_page, show_main

app_name = 'main'

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("homepage/", show_main, name="show_main"),
    path('', include(('discount.urls', 'discount'), namespace='discount')),
]