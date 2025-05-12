#cameras/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('buildings/create/', views.create_building, name='create_building'),
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/<int:building_id>/', views.building_detail, name='building_detail'),
    path('buildings/<int:building_id>/edit/', views.building_edit, name='building_edit'),
    path('cameras/<int:camera_id>/stream/', views.stream_camera, name='stream_camera'),
    path('cameras/<int:camera_id>/delete/', views.delete_camera, name='delete_camera'),
    path('api/regions/', views.region_list, name='region_list'),
    path('api/districts/', views.district_list, name='district_list'),
    path('api/districts/<int:region_id>/', views.district_list, name='district_list_by_region'),
    path('users/', views.users, name='users'),
    path('reports/', views.reports, name='reports'),
]