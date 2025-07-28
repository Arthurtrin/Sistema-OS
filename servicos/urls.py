from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
   path('listar/servicos/', views.listar_servicos, name='listar_servicos'),
   path('cadastrar/servico/', views.cadastrar_servico, name='cadastrar_servico'),
    
]