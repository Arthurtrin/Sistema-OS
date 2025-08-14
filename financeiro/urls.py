from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('principal/', views.principal, name='principal'),
]