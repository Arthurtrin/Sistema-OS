from django.db import models
from django.core.exceptions import ValidationError

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

class Empresa(models.Model):
    razao_social = models.CharField(max_length=60)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    logradouro = models.CharField(max_length=100, blank=False)
    numero = models.CharField(max_length=10, blank=False)
    complemento = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50, blank=False)
    cidade = models.CharField(max_length=50, blank=False)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='RJ', blank=False, null=False)
    cep = models.CharField(max_length=10, blank=False)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)  # <--- novo campo

    def save(self, *args, **kwargs):
        if not self.pk and Empresa.objects.exists():
            raise ValidationError("Já existe uma empresa cadastrada.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.razao_social}"
