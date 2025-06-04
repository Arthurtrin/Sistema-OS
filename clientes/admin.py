from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome_cliente', 'email1', 'cnpj_cpf', 'data_inclusao', 'cidade_real', 'estado_real')
    
    search_fields = ('codigo', 'nome_cliente', 'cnpj_cpf', 'cidade_real', 'estado_real')
    
    list_filter = ('estado_real', 'cidade_real', 'segmento')
