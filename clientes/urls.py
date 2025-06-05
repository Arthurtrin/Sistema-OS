from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('cadastrar_clientes/', views.cadastrar_clientes, name='cadastrar_clientes'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:cliente_id>/', views.excluir_cliente, name='excluir_cliente'),
    path('clientes/ver/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    path('segmento/editar/<int:seg_id>/', views.editar_segmento, name='editar_segmento'),
    path('segmento/excluir/<int:seg_id>/', views.excluir_segmento, name='excluir_segmento'),
    path('atividade/editar/<int:atv_id>/', views.editar_atividade, name='editar_atividade'),
    path('atividade/excluir/<int:atv_id>/', views.excluir_atividade, name='excluir_atividade'),
    path('segmentos/cadastrar/', views.cadastrar_segmento, name='cadastrar_segmento'),
    path('atividades/cadastrar/', views.cadastrar_atividade, name='cadastrar_atividade'),
    
    # Adicione outras rotas como editar, listar etc.
]