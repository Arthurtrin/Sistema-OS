from django.contrib import admin
from .models import AtividadeUsuarioCliente

@admin.register(AtividadeUsuarioCliente)
class AtividadeUsuarioClienteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cliente', 'descricao', 'data']