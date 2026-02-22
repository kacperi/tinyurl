from django.urls import path
from django.views.generic import TemplateView

from .views import CreateShortlinkView, redirect_to_page

urlpatterns = [
    path("short_link/", CreateShortlinkView.as_view()),
    path("redirect/", TemplateView.as_view(template_name="empty_hash.html")),
    path("redirect/<str:hash>/", redirect_to_page),
]
