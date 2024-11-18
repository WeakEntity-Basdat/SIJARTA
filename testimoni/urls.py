from django.urls import path
from . import views

urlpatterns = [
    path("subcategory/user/<int:subcategory_id>/", views.subcategory_user, name="subcategory_for_user"),
    path('buat_testimoni/<int:subcategory_id>/', views.buat_testimoni, name='buat_testimoni'),
]
