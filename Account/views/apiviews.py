from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User
from Account.api.serializers import UsuariosSerializer, ContaSerializer
from rest_framework import permissions
from Account.models import Conta
from rest_framework import status
from rest_framework.exceptions import PermissionDenied,ParseError

class UsuarioCriarListar(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer
    
    def get(self, request, *args, **kwargs):            
        if not self.request.user.is_superuser:
            raise PermissionDenied(detail="You need be admin to access this endpoint")
        return super().get(request, *args, **kwargs)

class ContaCriarListar(ListCreateAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

    def post(self, request, *args, **kwargs):
        id = self.request.user.id
        conta = Conta.objects.filter(usuario=id)
        if len(conta) == 0 and id == self.request.data["usuario"]:
            return super().post(request, *args, **kwargs)
        else:
            raise ParseError

    
    def get(self, request, *args, **kwargs):            
        if not self.request.user.is_superuser:
            raise PermissionDenied(detail="You need be admin to access this endpoint")

        return super().get(request, *args, **kwargs)


