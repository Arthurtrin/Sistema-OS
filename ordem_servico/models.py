from django.db import models
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

STATUS_CHOICES = [
    ('aberta', 'Aberta'),
    ('em_andamento', 'Em andamento'),
    ('aguardando', 'Aguardando peças'),
    ('finalizada', 'Finalizada'),
    ('cancelada', 'Cancelada'),
]

N_CLIENTE_CHOICES = [
    ('cliente_1', 'Cliente 1'),
    ('cliente_2', 'Cliente 2'),
    ('cliente_3', 'Cliente 3'),
    ('cliente_4', 'Cliente 4'),
]

DIGITADOR_CHOICES = [
    ('joao', 'João'),
    ('maria', 'Maria'),
    ('carlos', 'Carlos'),
    ('ana', 'Ana'),
]

UNIDADE_CHOICES = [
    ('unidade_a', 'Unidade A'),
    ('unidade_b', 'Unidade B'),
    ('unidade_c', 'Unidade C'),
    ('unidade_d', 'Unidade D'),
]

SEGMENTO_CHOICES = [
    ('eletrico', 'Elétrico'),
    ('civil', 'Civil'),
    ('hidraulico', 'Hidráulico'),
    ('automacao', 'Automação'),
]

# Create your models here.
class OrdemServico(models.Model):
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    titulo = models.CharField(max_length=100)
    data_abertura = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    n_cliente = models.CharField(max_length=50, choices=N_CLIENTE_CHOICES)
    digitador = models.CharField(max_length=50, choices=DIGITADOR_CHOICES)
    unidade = models.CharField(max_length=50, choices=UNIDADE_CHOICES)
    segmento = models.CharField(max_length=50, choices=SEGMENTO_CHOICES)
    solicitante = models.CharField(max_length=100)
    n_proposta = models.IntegerField()
    n_desenho = models.IntegerField()

    n_art = models.IntegerField()
    obra_inicio = models.DateTimeField()
    obra_termino = models.DateTimeField()
    obra_nome = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
    uc_os = models.CharField(max_length=100)
    oc = models.CharField(max_length=100)

    descricao = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='anexos/')

    def __str__(self):
        return f"{self.codigo}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Gera código automático com 8 caracteres únicos
            self.codigo = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)