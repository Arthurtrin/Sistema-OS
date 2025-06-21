from django.urls import path
from . import views

app_name = 'ordem_servico'

urlpatterns = [
    path('criar_os/', views.criar_os, name='criar_os'),
]