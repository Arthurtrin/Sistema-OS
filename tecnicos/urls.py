from django.urls import path
from . import views

app_name = 'tecnicos'

urlpatterns = [
    path('cadastrar/', views.cadastrar_tecnicos, name='cadastrar_tecnicos'),
    path('listar_tecnicos/', views.listar_tecnicos, name='listar_tecnicos'),
    path('editar_tecnico/<int:tecnico_id>/', views.editar_tecnico, name='editar_tecnico'),
    path('excluir_tecnico/<int:tecnico_id>/', views.excluir_tecnico, name='excluir_tecnico'),
    path('ver_tecnico/<int:tecnico_id>/', views.ver_tecnico, name='ver_tecnico'),
    # Exemplo:
    # path('', views.index, name='index'),
]