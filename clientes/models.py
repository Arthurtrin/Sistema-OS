from django.db import models

class Cliente(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    
    data_inclusao = models.DateTimeField()

    nome_cliente = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100, blank=True)
    
    email1 = models.EmailField()
    email2 = models.EmailField(blank=True, null=True)
    email3 = models.EmailField(blank=True, null=True)
    
    cnpj_cpf = models.CharField(max_length=18)
    
    telefone1 = models.CharField(max_length=20, blank=True)
    telefone2 = models.CharField(max_length=20, blank=True)
    celular1 = models.CharField(max_length=20, blank=True)
    celular2 = models.CharField(max_length=20, blank=True)
    
    inscricao_estadual = models.CharField(max_length=50)  
    inscricao_municipal = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome_cliente} ({self.codigo})"
