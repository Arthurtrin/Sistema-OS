from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    path('configuracao/empresa/', views.EmpresaUpdateView.as_view(), name='configuracao_empresa'),
]