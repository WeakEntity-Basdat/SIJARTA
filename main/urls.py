from django.urls import path, include

from main.views import landing_page, show_main,homepage
# subcategory_for_user, subcategory_for_worker, create_service_order, worker_profile, service_orders
app_name = 'main'

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("homepage/", homepage, name="show_main"),
    # path("subcategory/user/<int:subcategory_id>/", subcategory_for_user, name="subcategory_for_user"),
    # path("subcategory/worker/<int:subcategory_id>/", subcategory_for_worker, name="subcategory_for_worker"),
    # path("worker/profile/<int:worker_id>/", worker_profile, name="worker_profile"),
    path('', include(('discount.urls', 'discount'), namespace='discount')),
    # path('order/service/', create_service_order, name='create_service_order'),
    # path('service-orders/', service_orders, name='service_orders'),
]