from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('principal/', views.principal, name='principal'),
    path('empresas/', views.empresas, name='empresas'),
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/cadastrar/', views.cadastrar_fornecedor, name='cadastrar_fornecedor'),
    path('cadastrar/empresa/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('editar/empresa/<int:id>/', views.editar_empresa, name='editar_empresa'),
    path('excluir/empresa/<int:id>/', views.excluir_empresa, name='excluir_empresa'),
    path('cadastrar/formasdepagamento/cadastrar_forma_pagamento', views.cadastrar_forma_pagamento, name='cadastrar_forma_pagamento'),
    path('cadastrar/formasdepagamento/excluir_forma_pagamento/<int:id>/', views.excluir_forma_pagamento, name='excluir_forma_pagamento'),
    path('cadastrar/formasdepagamento/editar_forma_pagamento/<int:id>/', views.editar_forma_pagamento, name='editar_forma_pagamento'),
    
]