from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # URLs que não dependem de idioma, por exemplo:
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('usuarios.urls')),
    path('painel/', include('principal.urls')),
    path('clientes/', include('clientes.urls')),
    path('tecnicos/', include('tecnicos.urls')),
    path('atividades/', include('atividades.urls')),
    path('produtos/', include('produtos.urls')),
    path('ordem_servico/', include('ordem_servico.urls')),
   
)
