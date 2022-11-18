from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from Account.api.serializers import UsuariosSerializer, ContaSerializer
from rest_framework import permissions
from Account.models import Conta
from rest_framework import status
from rest_framework.exceptions import PermissionDenied,ParseError

class UsuarioDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer

class UsuarioCriarListar(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer
    
    def get(self, request, *args, **kwargs):            
        if not self.request.user.is_superuser:
            raise PermissionDenied(detail="Você precisa ser admin ter acesso.")
        return super().get(request, *args, **kwargs)


class ContaDetail(RetrieveUpdateDestroyAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer


class ContaCriarListar(ListCreateAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

    def post(self, request, *args, **kwargs):
        id = self.request.user.id
        conta = Conta.objects.filter(usuario=id)
        if len(conta) == 0 and id == self.request.data["usuario"]:
            return super().post(request, *args, **kwargs)
        else:
            raise ParseError(detail="Você já tem uma conta")

    
    def get(self, request, *args, **kwargs):            
        if not self.request.user.is_superuser:
            raise PermissionDenied(detail="Você precisa ser admin ter acesso.")

        return super().get(request, *args, **kwargs)


