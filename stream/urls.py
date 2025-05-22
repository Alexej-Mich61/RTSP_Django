#stream/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cameras/', include('cameras.urls')),  # Убедись, что 'cameras.urls' подключён
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
]