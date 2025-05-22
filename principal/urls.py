from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/<str:usuario>', views.usuarios, name='usuarios'),
]