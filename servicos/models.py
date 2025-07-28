from django.db import models
from tecnicos.models import Tecnico

class Servico(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=10)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return self.nome