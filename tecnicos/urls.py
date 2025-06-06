from django.urls import path
from . import views

app_name = 'tecnicos'

urlpatterns = [
    path('cadastrar/', views.cadastrar_tecnicos, name='cadastrar_tecnicos'),
    # Exemplo:
    # path('', views.index, name='index'),
]