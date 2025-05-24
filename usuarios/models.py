from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('normal', 'Usuário Normal'),
        ('supervisor', 'Supervisor'),
        ('gerenciador', 'Gerenciador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='normal')

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo}'


class Chave_Gerenciador(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE)
    chave = models.CharField(max_length=20, default='')

    def __str__(self):
        return f'{self.nome} - {self.chave}'
