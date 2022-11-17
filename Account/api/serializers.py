from rest_framework import serializers
from Account.models import Usuarios


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        queryset = Usuarios.objects.all()