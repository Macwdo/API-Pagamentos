from rest_framework import serializers
from Account.models import Conta
from django.contrib.auth.models import User
from rest_framework import status
import re
from rest_framework.exceptions import ValidationError


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = "__all__"
    
    def validate_cpf(self,value):
        regex = re.compile(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})")
        if regex.match(value) is None:
            raise ValidationError("cpf não é valido",code=status.HTTP_406_NOT_ACCEPTABLE)
        return value


class UsuariosSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username","email","password","password2") 

    def save(self, *args,**kwargs):
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
