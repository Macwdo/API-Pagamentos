from django.db import models
# Create your models here.


class Instituicao(models.Model):
    nome_instituicao = models.CharField(max_length=50)


class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11,unique=True)
    conta = models.FloatField(default=0)
    instituicao = models.ForeignKey(Instituicao,on_delete=)

class Transferencia(models.Model):
    origem = models.ForeignKey(Usuarios)
    destino = models.CharField(max_length=11)
    valor = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    