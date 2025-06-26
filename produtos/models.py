from django.db import models

class Grupo(models.Model):
    nome = models.CharField(max_length=60)
    def __str__(self):
        return self.nome

class Marca(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Fabricante(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Produto(models.Model):
    #sera feito em definiçoes
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('fora_de_linha', 'Fora de linha'),
        ('ruptura', 'Ruptura'),
        ('preco_desatualizado', 'Preço desatualizado'),
        ('consumo_proprio', 'Consumo próprio'),
        ('nao_comercializado', 'Não comercializado'),
    ]

    # Identificação
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nome = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)

    quantidade = models.IntegerField(default=0)
    qtd_entrada = models.IntegerField()
    estoque_minimo = models.IntegerField()
    estoque_maximo = models.IntegerField()
    situacao = models.CharField(max_length=30, choices=SITUACAO_CHOICES, default='ativo')

    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    ref_fabricante = models.CharField(max_length=100)

    cod_embalagem = models.CharField(max_length=20, unique=True, blank=True, null=True)
    cod_barra = models.CharField(max_length=50)
    apresentacao = models.CharField(max_length=60)
    data_ultima_compra = models.DateField(blank=True, null=True)

    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
