from django.urls import path
from . import views

app_name = 'ordem_servico'

urlpatterns = [
    path('criar_os/', views.criar_os, name='criar_os'),
    path('os/ver/<int:os_id>/', views.ver_os, name='ver_os'),
    path('definicao/', views.definicao, name='definicao'),
    
     # Segmentos
    path('cadastrar_segmento/', views.cadastrar_segmento, name='cadastrar_segmento'),
    path('editar_segmento/<int:segmento_id>/', views.editar_segmento, name='editar_segmento'),
    path('excluir_segmento/<int:segmento_id>/', views.excluir_segmento, name='excluir_segmento'),

    # Unidades
    path('cadastrar_unidade/', views.cadastrar_unidade, name='cadastrar_unidade'),
    path('editar_unidade/<int:unidade_id>/', views.editar_unidade, name='editar_unidade'),
    path('excluir_unidade/<int:unidade_id>/', views.excluir_unidade, name='excluir_unidade'),

    # Status
    path('cadastrar_status/', views.cadastrar_status, name='cadastrar_status'),
    path('editar_status/<int:status_id>/', views.editar_status, name='editar_status'),
    path('excluir_status/<int:status_id>/', views.excluir_status, name='excluir_status'),
    
]