from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('principal/', views.principal, name='principal'),
    path('empresas/', views.empresas, name='empresas'),

    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('editar/fornecedor/<int:id>/', views.editar_fornecedores, name='editar_fornecedores'),
    path('excluir/fornecedor/<int:id>/', views.excluir_fornecedores, name='excluir_fornecedores'),
    path('fornecedores/cadastrar/', views.cadastrar_fornecedor, name='cadastrar_fornecedor'),

    path('cadastrar/empresa/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('editar/empresa/<int:id>/', views.editar_empresa, name='editar_empresa'),
    path('excluir/empresa/<int:id>/', views.excluir_empresa, name='excluir_empresa'),

    path('cadastrar/formasdepagamento/cadastrar_forma_pagamento', views.cadastrar_forma_pagamento, name='cadastrar_forma_pagamento'),
    path('cadastrar/formasdepagamento/excluir_forma_pagamento/<int:id>/', views.excluir_forma_pagamento, name='excluir_forma_pagamento'),
    path('cadastrar/formasdepagamento/editar_forma_pagamento/<int:id>/', views.editar_forma_pagamento, name='editar_forma_pagamento'),
    
    path('cadastrar/local-cobranca/', views.locais_cobranca, name='locais_cobranca'),
    path('cadastrar/cobranca/excluir_locais_cobranca/<int:id>/', views.excluir_locais_cobranca, name='excluir_locais_cobranca'),
    path('cadastrar/cobranca/editar_locais_cobranca/<int:id>/', views.editar_locais_cobranca, name='editar_locais_cobranca'),

    path('receitas/', views.receitas, name='receitas'),
    path('receitas/cadastrar', views.cadastrar_receita, name='cadastrar_receita'),
    path('receitas/excluir/<int:id>/', views.excluir_receita, name='excluir_receita'),
    path('receitas/editar/<int:id>/', views.editar_receita, name='editar_receita'),
]