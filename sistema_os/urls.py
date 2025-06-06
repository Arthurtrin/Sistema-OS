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
<<<<<<< HEAD
    path('tecnicos/', include('tecnicos.urls')),
=======
>>>>>>> ba9e299152ba5cd0e8466fd872595f1fc748b708
)
