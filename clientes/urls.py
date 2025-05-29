from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('cadastrar_clientes/', views.cadastrar_clientes, name='cadastrar_clientes'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:cliente_id>/', views.excluir_cliente, name='excluir_cliente'),
    path('clientes/ver/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    # Adicione outras rotas como editar, listar etc.
]