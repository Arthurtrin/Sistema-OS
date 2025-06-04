from django.db import models

class Atividade(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nome}"

class Segmento(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nome}"
