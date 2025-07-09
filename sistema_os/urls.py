from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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
    path('configuracoes/', include('configuracoes.urls')),
)

# Adicione isso no final do arquivo, fora do bloco do i18n_patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
