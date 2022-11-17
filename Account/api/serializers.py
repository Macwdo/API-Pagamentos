from rest_framework import serializers
from Account.models import Conta
from django.contrib.auth.models import User


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = "__all__"

class UsuariosSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    class Meta:
        model = User
        fields = ("username","email","password")
        
        
        