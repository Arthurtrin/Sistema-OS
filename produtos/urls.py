from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/ver/', views.listar_produtos, name='listar_produtos'),
    path('produtos/fabricante_marca/', views.fabricante_marca_grupo, name='fabricante_marca_grupo'),
    path('produtos/marca/editar/<int:marca_id>/', views.editar_marca, name='editar_marca'),
    path('produtos/fabricante/editar/<int:fabricante_id>/', views.editar_fabricante, name='editar_fabricante'),
    path('produtos/marca/excluir/<int:marca_id>/', views.excluir_marca, name='excluir_marca'),
    path('produtos/fabricante/excluir/<int:fabricante_id>/', views.excluir_fabricante, name='excluir_fabricante'),
    path('produtos/marca/cadastrar/', views.cadastrar_marca, name='cadastrar_marca'),
    path('produtos/fabricante/cadastrar/', views.cadastrar_fabricante, name='cadastrar_fabricante'),
    path('produtos/grupo/editar/<int:grupo_id>', views.editar_grupo, name='editar_grupo'),
    
]