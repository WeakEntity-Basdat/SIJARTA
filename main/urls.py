from django.urls import path

from main.views import landing_page, show_main

app_name = 'main'

urlpatterns = [
    path("landingpage/", landing_page, name="landing_page"),
    path("homepage/", show_main, name="show_main"),
]