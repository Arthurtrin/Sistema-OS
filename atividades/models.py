from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente

class AtividadeUsuarioCliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.cliente.nome_cliente}"