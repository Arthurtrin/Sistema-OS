from django.db import models
from clientes.models import Cliente
from produtos.models import Produto
from django.contrib.auth.models import User
import uuid

# Choices para estados brasileiros
ESTADOS = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]


class Segmento(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Unidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Status(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Create your models here.
class OrdemServico(models.Model):
    
    titulo = models.CharField(max_length=100)
    data_abertura = models.DateField()
    
    n_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    digitador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    segmento = models.ForeignKey(Segmento, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    solicitante = models.CharField(max_length=100)
    n_proposta = models.IntegerField()
    n_desenho = models.IntegerField()

    n_art = models.IntegerField()
    obra_inicio = models.DateField()
    obra_termino = models.DateField(null=True, blank=True)
    obra_nome = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
    uc_os = models.CharField(max_length=100)
    oc = models.CharField(max_length=100)

    descricao = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='anexos/')

    def __str__(self):
        return f"{self.codigo}"


class ProdutoOrdemServico(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    baixa = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.produto.nome} (x{self.quantidade})'