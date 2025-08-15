from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('principal/', views.principal, name='principal'),
    path('cadastrar/empresa/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('cadastrar/formasdepagamento/', views.forma_pg, name='forma_pg'),
    path('cadastrar/formasdepagamento/cadastrar_forma_pagamento', views.cadastrar_forma_pagamento, name='cadastrar_forma_pagamento'),
    path('cadastrar/formasdepagamento/excluir_forma_pagamento/<int:id>/', views.excluir_forma_pagamento, name='excluir_forma_pagamento'),
    path('cadastrar/formasdepagamento/editar_forma_pagamento/<int:id>/', views.editar_forma_pagamento, name='editar_forma_pagamento'),
    
]