import re
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from Account.models import Conta, Instituicao, Transferencia

def cpf_validation(value):
    regex = re.compile(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})")
    if regex.match(value) is None:
        raise ValidationError(detail={"cpf": "cpf não é valido"})
    return value

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
        cpf_validation(value)
        return value

    def validate_saldo(self, value):
        return value


class UsuariosSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2",)

    def validate(self, attrs):
        if attrs["password"] == attrs["password2"]:
            return super().validate(attrs)
        else:
            raise ValidationError(detail="As senhas são diferentes")

    def save(self, *args, **kwargs):
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            password=self.validated_data["password"],
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user

class TransferenciaSerializer(serializers.ModelSerializer):
    instituicao_origem = serializers.StringRelatedField(source="origem.instituicao", read_only=True)
    instituicao_destinatario = serializers.StringRelatedField(source="destino.instituicao", read_only=True)
    cpf_origem = serializers.CharField(source="origem.cpf",max_length=11, allow_blank=False)
    cpf_destino = serializers.CharField(source="destino.cpf",max_length=11, allow_blank=False)


    class Meta:
        model = Transferencia
        fields = (
            "cpf_origem", "cpf_destino",
            "instituicao_origem", "instituicao_destinatario",
            "valor", "data",
        )

    def validate_cpf_origem(self, value):
        cpf_validation(value)
        return value

    def validate_cpf_destino(self, value):
        cpf_validation(value)
        return value

    def save(self, *args, **kwargs):
        try:
            origem = Conta.objects.get(cpf=self.validated_data["origem"]["cpf"])
            destino = Conta.objects.get(cpf=self.validated_data["destino"]["cpf"])
        except Conta.DoesNotExist:
            print(self.validated_data)
            raise ValidationError({"conta": "Error ao Informar a conta"})
        valor = self.validated_data["valor"]
        if origem.saldo >= valor:
            origem.saldo -= valor
            destino.saldo += valor
            origem.save()
            destino.save()
        else:
            raise ValidationError(detail={"saldo": "Conta informada não tem saldo suficiente"})
        transferencia = Transferencia.objects.create(
            origem=origem,
            destino=destino,
            valor=self.validated_data["valor"],
        )
        return transferencia
