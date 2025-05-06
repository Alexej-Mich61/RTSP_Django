#stream/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cameras/', include('cameras.urls')),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
]