from django.contrib import admin
from .models import ContasReceber,  Empresa, FormaPagamento, Fornecedor, LocalCobranca
# Register your models here.

admin.site.register(ContasReceber)
admin.site.register(Empresa)
admin.site.register(FormaPagamento)
admin.site.register(Fornecedor)
admin.site.register(LocalCobranca)

