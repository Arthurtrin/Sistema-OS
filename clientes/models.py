from django.db import models
<<<<<<< HEAD
import uuid
=======

>>>>>>> ba9e299152ba5cd0e8466fd872595f1fc748b708

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

class Atividade(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nome}"

class Segmento(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nome}"

class Cliente(models.Model):
    # Identificação
<<<<<<< HEAD
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nome_cliente = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100, blank=True)
    data_inclusao = models.DateTimeField()
    cnpj_cpf = models.CharField(max_length=18, unique=True)
=======
    codigo = models.CharField(max_length=20, unique=True)
    nome_cliente = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100, blank=True)
    data_inclusao = models.DateTimeField()
    cnpj_cpf = models.CharField(max_length=18)
>>>>>>> ba9e299152ba5cd0e8466fd872595f1fc748b708
    inscricao_estadual = models.CharField(max_length=50)  
    inscricao_municipal = models.CharField(max_length=50)
    
    # Contato
    email1 = models.EmailField()
    email2 = models.EmailField(blank=True, null=True)
    telefone1 = models.CharField(max_length=20, blank=True)
    telefone2 = models.CharField(max_length=20, blank=True)
    celular1 = models.CharField(max_length=20, blank=True)
    celular2 = models.CharField(max_length=20, blank=True)

    # Filtros
    atividade = models.ForeignKey(Atividade, on_delete=models.SET_NULL, blank=False, null=True)
    segmento = models.ForeignKey(Segmento, on_delete=models.SET_NULL, blank=False, null=True)
    observacao = models.TextField(blank=True, null=True)

    # Endereço Real - obrigatório
    logradouro_real = models.CharField(max_length=100, blank=False)
    numero_real = models.CharField(max_length=10, blank=False)
    complemento_real = models.CharField(max_length=50, blank=True)
    bairro_real = models.CharField(max_length=50, blank=False)
    cidade_real = models.CharField(max_length=50, blank=False)
<<<<<<< HEAD
    estado_real = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
=======
    estado_real = models.CharField(max_length=2, choices=ESTADOS, default='-', blank=False, null=False)
>>>>>>> ba9e299152ba5cd0e8466fd872595f1fc748b708
    cep_real = models.CharField(max_length=10, blank=False)


    # Endereço2
    logradouro_cobranca = models.CharField(max_length=100, blank=True)
    numero_cobranca = models.CharField(max_length=10, blank=True)
    complemento_cobranca = models.CharField(max_length=50, blank=True)
    bairro_cobranca = models.CharField(max_length=50, blank=True)
    cidade_cobranca = models.CharField(max_length=50, blank=True)
    estado_cobranca = models.CharField(max_length=2, choices=ESTADOS, blank=True, null=True)
    cep_cobranca = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.nome_cliente} ({self.codigo})"

<<<<<<< HEAD
    def save(self, *args, **kwargs):
        if not self.codigo:
            # Gera código automático com 8 caracteres únicos
            self.codigo = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


=======
>>>>>>> ba9e299152ba5cd0e8466fd872595f1fc748b708

