from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('ver_atividades/', views.ver_atividades, name='ver_atividades'),

]