from django.urls import path, include

from main.views import landing_page, show_main, subcategory_for_user, subcategory_for_worker, create_service_order

app_name = 'main'

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("homepage/", show_main, name="show_main"),
    path("subcategory/user/<int:subcategory_id>/", subcategory_for_user, name="subcategory_for_user"),
    path("subcategory/worker/<int:subcategory_id>/", subcategory_for_worker, name="subcategory_for_worker"),
    path('', include(('discount.urls', 'discount'), namespace='discount')),
    path('order/service/', create_service_order, name='create_service_order'),
]