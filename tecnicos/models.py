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

class Tecnico(models.Model):
    nome = models.CharField(max_length=100)
    

    cnpj_cpf = models.CharField(max_length=18, unique=True)
    rg = models.CharField(max_length=18, unique=True)

    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)

    comissao = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        help_text="Porcentagem de comissão (ex: 10.00 para 10%)"
    )

    # Endereço
    logradouro = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=True)
    cep = models.CharField(max_length=10, blank=True)

    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
   

