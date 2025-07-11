from django.contrib import admin
from .models import OrdemServico, ProdutoOrdemServico, Segmento, Unidade, Status

class ProdutoOrdemServicoInline(admin.TabularInline):
    model = ProdutoOrdemServico
    extra = 1  # Quantos campos em branco aparecerão para adicionar novos produtos
    autocomplete_fields = ['produto']  # Se tiver muitos produtos, isso ajuda bastante

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_abertura', 'status']
    search_fields = ['titulo', 'n_cliente__nome_cliente']
    list_filter = ['status', 'data_abertura', 'uf']
    inlines = [ProdutoOrdemServicoInline]

# Simples registro dos modelos auxiliares
@admin.register(Segmento)
class SegmentoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']