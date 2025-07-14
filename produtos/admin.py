from django.contrib import admin
from .models import Produto, Grupo, Marca, Fabricante, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo', 'fabricante', 'marca', 'situacao', 'data_ultima_compra')
    list_filter = ('situacao', 'grupo', 'fabricante', 'marca')
    search_fields = ('nome', 'codigo', 'cod_barra')

admin.site.register(Grupo)
admin.site.register(Marca)
admin.site.register(Fabricante)
admin.site.register(Movimentacao)
