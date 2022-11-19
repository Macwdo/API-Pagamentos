from criar_models import AccountUtils
from rest_framework import test
from Account.permissions import Dono
from django.contrib.auth.models import User
from Account.models import Transferencia, Instituicao, Conta
from django.urls import reverse


class ContasTestes(test.APITestCase, AccountUtils):
    
    def test_permission_dono(self):
        usuario = self.make_usuario()
        conta = self.make_conta(usuario=usuario)
        response = self.client.get(reverse("Account:detail-usuarios",kwargs={"pk":1}))
        print(response.cookies.values())
        assert 1 == 1
        
