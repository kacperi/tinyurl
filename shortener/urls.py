from django.urls import path
from .views import create_shortlink

urlpatterns = [
    path("short_link/", create_shortlink),
]
