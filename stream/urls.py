#stream/urls.py
import logging
from django.contrib import admin
from django.urls import path, include
from cameras import views

logger = logging.getLogger(__name__)
logger.info("Загрузка stream.urls")

# Инициализация маршрутов
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cameras/', include('cameras.urls')),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
    path('log-camera-play/', views.log_camera_play),
]

# Дополнительная отладка
logger.debug("Маршруты stream: %s", urlpatterns)

# Отладка маршрутов после инициализации
def log_url_patterns():
    from django.urls import get_resolver
    resolver = get_resolver()
    logger.debug("Доступные маршруты: %s", resolver.url_patterns)

if __name__ == '__main__':
    log_url_patterns()