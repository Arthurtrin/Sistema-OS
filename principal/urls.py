from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/<str:usuario>', views.usuarios, name='usuarios'),
    path('ordem_servico/', views.ordem_servico, name='ordem_servico'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('novo-template/', views.novo_template, name='novo_template'),
    path('os/', views.os, name='os'),
    
]