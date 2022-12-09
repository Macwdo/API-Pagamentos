from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Instituicao(models.Model):
    nome_instituicao = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_instituicao

class Conta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    saldo = models.FloatField(default=0)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

class Transferencia(models.Model):
    origem = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="Origem")
    destino = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="Destinatario")
    valor = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origem.nome} - {self.destino.nome}"
