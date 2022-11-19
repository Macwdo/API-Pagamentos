import re

from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from Account.models import Conta, Instituicao


class ContaSerializer(serializers.ModelSerializer):
    nome_usuario = serializers.StringRelatedField(source="usuario", read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    banco = serializers.StringRelatedField(source="instituicao", read_only=True)
    instituicao = serializers.PrimaryKeyRelatedField(queryset=Instituicao.objects.all(), write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conta
        fields = ("id", "cpf", "nome", "saldo", "banco", "nome_usuario", "instituicao", "usuario")

    def validate_cpf(self, value):
        regex = re.compile(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})")
        if regex.match(value) is None:
            raise ValidationError("cpf não é valido", code=status.HTTP_406_NOT_ACCEPTABLE)
        return value

    def validate_saldo(self, value):
        value = 0
        return value


class UsuariosSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2",)

    def save(self, *args, **kwargs):
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            password=self.validated_data["password"],
        )
        if self.validated_data["password"] != self.validated_data["password2"]:
            raise ValidationError("As senhas são diferentes")

        user.set_password(self.validated_data["password"])
        user.save()
        return user
