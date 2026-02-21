from django.urls import path
from django.views.generic import TemplateView

from .views import create_shortlink, redirect_to_page

urlpatterns = [
    path("short_link/", create_shortlink),
    path("redirect/", TemplateView.as_view(template_name="shortener/index.html")),
    path("redirect/<str:hash>/", redirect_to_page),
]
