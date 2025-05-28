from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome_cliente', 'email1', 'cnpj_cpf', 'data_inclusao')
    search_fields = ('codigo', 'nome_cliente', 'cnpj_cpf')
