from django.urls import path, include

from main.views import landing_page, show_main, homepage_pelanggan, homepage_pekerja, subcategory_detail, homepage
# subcategory_for_user, subcategory_for_worker, create_service_order, worker_profile, service_orders
from . import views
app_name = 'main'

urlpatterns = [
    # path("", landing_page, name="landing_page"),
    # path("homepage/", show_main, name="show_main"),
    path('homepage/', homepage, name='homepage'),
    path('homepage-pelanggan/', homepage_pelanggan, name='homepage_pelanggan'),
    path('homepage-pekerja/', homepage_pekerja, name='homepage_pekerja'),
    path('subkategori/<uuid:subcategory_id>/', views.subcategory_detail, name='subcategoryjasa_pelangan'),
    path('pekerja/<uuid:worker_id>/', views.worker_profile, name='worker_profile'),
    path('order_service/<uuid:session_id>/', views.create_order, name='order_service'),
    path('view_orders/', views.view_orders, name='view_orders'),
    # path('homepage/', homepage, name='homepage'),
    # path("subcategory/user/<int:subcategory_id>/", subcategory_for_user, name="subcategory_for_user"),
    # path("subcategory/worker/<int:subcategory_id>/", subcategory_for_worker, name="subcategory_for_worker"),
    # path("worker/profile/<int:worker_id>/", worker_profile, name="worker_profile"),
    path('subcategory/<uuid:subcategory_id>/', subcategory_detail, name='subcategory_detail'),
    path('', include(('discount.urls', 'discount'), namespace='discount')),
    # path('order/service/', create_service_order, name='create_service_order'),
    # path('service-orders/', service_orders, name='service_orders'),
    # path('subcategory-detail/', subcategory_detail, name='subcategory_detail'),
]