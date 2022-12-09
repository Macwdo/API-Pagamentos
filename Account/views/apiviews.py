from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.exceptions import (AuthenticationFailed, ParseError,
                                       PermissionDenied)
from rest_framework.generics import (ListCreateAPIView,
 
                                     RetrieveUpdateDestroyAPIView)
#from rest_framework.pagination import PageNumberPagination

from Account.api.serializers import ContaSerializer, UsuariosSerializer, TransferenciaSerializer
from Account.models import Conta, Transferencia
from Account.permissions import Dono

# class MyPagination(PageNumberPagination): Alterando atributo da classe de paginação
#     page_size = 10

class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer

class UserCreateList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer
    # pagination_class = MyPagination


class AccountDetail(RetrieveUpdateDestroyAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [Dono]

    def patch(self, request, *args, **kwargs):
        campos = {
            "cpf": request.data.get("cpf", None),
            "saldo": request.data.get("saldo", None),
            "nome": request.data.get("nome", None),
            "instituicao": request.data.get("instituicao", None)
        }
        for key, values in campos.items():
            if values is not None:
                if request.user.is_superuser:
                    return super().patch(request, *args, **kwargs)
                raise PermissionDenied(f"Não é possível alterar o campo de {key}", code=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        campos_request = {
            "cpf": request.data.get("cpf", None),
            "saldo": request.data.get("saldo", None),
            "usuario": request.data.get("usuario",None),
            "instituicao": request.data.get("instituicao", None)

        }

        if int(request.user.id) != int(campos_request["usuario"]):
            raise AuthenticationFailed(f"Você não é o Dono desta Conta")

        conta = Conta.objects.get(id=self.kwargs.get("pk"))
        campos_conta = (conta.cpf, conta.saldo, conta.usuario.pk, conta.instituicao)

        for valor_conta, valor_request_key, valor_request_value in zip(campos_conta, campos_request.keys(), campos_request.values()):
            if not request.user.is_superuser:
                if valor_conta == valor_request_value:
                    return super().put(request, *args, **kwargs)
                raise PermissionDenied(f"Não é possível alterar o campo de {valor_request_key}")
        return super().put(request, *args, **kwargs)


class AccountCreateList(ListCreateAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    # pagination_class = MyPagination

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes.append(permissions.IsAdminUser)

        if self.request.method == "POST":
            self.permission_classes.clear()

        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise AuthenticationFailed(detail="Você precisa estar logado para fazer isso")
        id = self.request.user.id
        request.data["usuario"] = id

        conta = Conta.objects.filter(usuario=id)
        if len(conta) == 0 and self.request.data["usuario"] == id or request.user.is_superuser:
            return super().post(request, *args, **kwargs)
        else:
            raise ParseError(detail="Você já tem uma conta")

class TransferCreateList(ListCreateAPIView):
    queryset = Transferencia.objects.all()
    serializer_class = TransferenciaSerializer

    
