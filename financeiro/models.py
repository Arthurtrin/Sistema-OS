from django.db import models
from clientes.models import Cliente

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

class Empresa(models.Model):
    empresa = models.CharField(max_length=100)
    nome = models.CharField(max_length=60)
    cnpj = models.CharField(max_length=18) 
    insc_municipal = models.CharField(max_length=10)
    insc_estadual = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
    telefone = models.CharField(max_length=20)
    cep = models.CharField(max_length=9)
    email = models.CharField(max_length=60)
    
    def __str__(self):
        return self.empresa

class FormaPagamento(models.Model):
    forma = models.CharField(max_length=30)

    def __str__(self):
        return self.forma

class LocalCobranca(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    STATUS = [
    ('ativo', 'Ativo'),
    ('inativo', 'Inativo'),
    ]
    nome = models.CharField(max_length=60)
    razao_social = models.CharField(max_length=100)
    insc_municipal = models.CharField(max_length=50)
    insc_estadual = models.CharField(max_length=50)
    cnpj_cpf = models.CharField(max_length=50)
    rg = models.CharField(max_length=50)
    ativo =  models.CharField(max_length=7, choices=STATUS, default='ativo', blank=False, null=False)
    email = models.CharField(max_length=60)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=20)

    conta_corrente = models.IntegerField(blank=True, null=True)
    agencia = models.IntegerField(blank=True, null=True)
    n_banco = models.IntegerField(blank=True, null=True)
    prazo_entrega = models.IntegerField(blank=True, null=True)
    margem_lucro = models.IntegerField(blank=True, null=True)

    contato_tel1 = models.CharField(max_length=20, blank=True, null=True)
    contato_tel2 = models.CharField(max_length=20, blank=True, null=True)
    contato_tel3 = models.CharField(max_length=20, blank=True, null=True)
    contato_tel4 = models.CharField(max_length=20, blank=True, null=True)

    forma_pgto = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    observacao = models.TextField()

    def __str__(self):
        return self.razao_social




# Create your models here.
class ContasReceber(models.Model):

    #INTEGER
    natureza = models.IntegerField()
    cfop = models.IntegerField()

    #FLOAT
    valor_total = models.FloatField()
    desconto = models.FloatField()
    iss = models.FloatField()
    valor_final = models.FloatField()
    icms = models.FloatField()
    vl_desconto = models.FloatField()
    vl_iss = models.FloatField()
    vl_icms = models.FloatField()
    juros = models.FloatField()
    vl_ipi = models.FloatField()
    imp_ret_fonte = models.FloatField()
    vl_duplicata = models.FloatField()

    #CHAR
    n_documento = models.CharField(max_length=60)
    n_duplicata = models.CharField(max_length=60)
    praca = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
    serie = models.CharField(max_length=60)
    
    historico = models.TextField()
    cobranca = models.CharField(max_length=60)
    n_bol_emp = models.CharField(max_length=60) 
    vendedor_1 = models.CharField(max_length=60)
    vendedor_2 = models.CharField(max_length=60)

    #FOREINGKEY
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    forma_pgto = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    
    #DATA
    emissao = models.DateField()
    vencimento = models.DateField()
    data_programada = models.DateField()
    
    '''
    fluxo_caixa e mov_estoque são opções para futuramente
    fazer a baixa no estoque ou tirar do fluxo de caixa

    '''

    def __str__(self):
        return self.n_documento