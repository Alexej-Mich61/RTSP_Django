#cameras/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('buildings/create/', views.building_create, name='building_create'),
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),  # Изменено building_id на pk
    path('buildings/<int:pk>/edit/', views.building_edit, name='building_edit'),
    path('cameras/<int:camera_id>/stream/', views.stream_camera, name='stream_camera'),
    path('cameras/<int:camera_id>/delete/', views.delete_camera, name='delete_camera'),
    path('api/regions/', views.region_list, name='region_list'),
    path('api/districts/<int:region_id>/', views.get_districts, name='district_list_by_region'),
]