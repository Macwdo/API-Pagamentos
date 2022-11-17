from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from Account.api.serializers import UsuariosSerializer, ContaSerializer
from rest_framework import permissions
from Account.models import Conta


class CriarUsuario(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer

class CriarConta(CreateAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer


