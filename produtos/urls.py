from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/ver/', views.listar_produtos, name='listar_produtos'),

]