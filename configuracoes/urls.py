from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    path('configuracao/empresa/', views.EmpresaUpdateView.as_view(), name='configuracao_empresa'),
    path('configuracao/usuario/', views.usuario, name='usuario'),
    path('configuracao/usuario/editar/<int:id>', views.editar_usuario, name='editar_usuario'),
]