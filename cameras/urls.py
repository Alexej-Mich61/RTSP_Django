#cameras/urls.py
import logging
from django.urls import path
from django.http import HttpResponse
from . import views

logger = logging.getLogger(__name__)
logger.info("Загрузка cameras.urls")

# Тестовый маршрут
def test_view(request):
    return HttpResponse("Тестовый маршрут работает!")

urlpatterns = [
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),
    path('buildings/create/', views.building_create, name='building_create'),
    path('buildings/<int:pk>/edit/', views.building_edit, name='building_edit'),
    path('cameras/<int:camera_id>/delete/', views.delete_camera, name='delete_camera'),
    path('regions/', views.region_list, name='region_list'),
    path('districts/<int:region_id>/', views.get_districts, name='get_districts'),
    path('get_cameras/<int:building_id>/', views.get_cameras, name='get_cameras'),
    path('stream/<int:camera_id>/', views.stream_camera, name='stream_camera'),
    path('log-camera-play/', views.log_camera_play, name='log_camera_play'),
    path('test/', test_view, name='test_view'),
]

# Дополнительная отладка
logger.debug("Маршруты cameras: %s", [pattern.pattern for pattern in urlpatterns])