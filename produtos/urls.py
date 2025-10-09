from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/ver/', views.listar_produtos, name='listar_produtos'),
    path('produto/excluir/<int:produto_id>', views.excluir_produto, name='excluir_produto'),
    path('produto/editar/<int:produto_id>', views.editar_produto, name='editar_produto'),
    path('produto/entrada', views.entrada_produto, name='entrada_produto'),
    path('produto/saida', views.saida_produto, name='saida_produto'),
    path('produto/ver/<int:produto_id>/', views.ver_produto, name='ver_produto'),
    path('produtos/fabricante_marca/', views.fabricante_marca_grupo, name='fabricante_marca_grupo'),
    path('produtos/movimentacao/relatorio', views.relatorio_movimentacao, name='relatorio_movimentacao'),
    path('produtos/marca/editar/<int:marca_id>/', views.editar_marca, name='editar_marca'),
    path('produtos/fabricante/editar/<int:fabricante_id>/', views.editar_fabricante, name='editar_fabricante'),
    path('produtos/marca/excluir/<int:marca_id>/', views.excluir_marca, name='excluir_marca'),
    path('produtos/fabricante/excluir/<int:fabricante_id>/', views.excluir_fabricante, name='excluir_fabricante'),
    path('produtos/marca/cadastrar/', views.cadastrar_marca, name='cadastrar_marca'),
    path('produtos/fabricante/cadastrar/', views.cadastrar_fabricante, name='cadastrar_fabricante'),
    path('produtos/grupo/cadastrar/', views.cadastrar_grupo, name='cadastrar_grupo'),
    path('produtos/grupo/editar/<int:grupo_id>', views.editar_grupo, name='editar_grupo'),
    path('produtos/grupo/excluir/<int:grupo_id>', views.excluir_grupo, name='excluir_grupo'),
    path('lista-de-produtos', views.lista_de_produtos, name='lista_de_produtos'),
    path('consultar', views.consultar_produto, name='consultar_produto'),
    
]