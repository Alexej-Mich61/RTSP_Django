#reports/urls.py
from django.urls import path
from cameras import views

urlpatterns = [
    path('', views.users, name='users'),
]