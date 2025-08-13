from django.urls import path
from . import views

urlpatterns = [
    path('', views.novo_template, name='novo_template'),
    path('os/', views.home, name='home'),
    path('usuarios/<str:usuario>', views.usuarios, name='usuarios'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]