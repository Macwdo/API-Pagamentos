from criar_models import AccountUtils
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import test

from Account.models import Conta, Instituicao, Transferencia
from Account.permissions import Dono


class ContasTestes(test.APITestCase, AccountUtils):


    def get_jwt_token(self, username="testename", password="testesenha"):
        data = {
            "username": username,
            "password": password
        }

        token = self.client.post(reverse("Account:token"), data=data)
        return token.data["access"]

    def test_permission_dono(self):
        usuario = self.make_usuario()
        token = self.get_jwt_token()
        url = reverse("Account:list-usuarios")
        data = {"cpf":12303122232}
        response = self.client.post(
            reverse("Account:list-conta"),
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
                        
            )
        print(response)

        assert 1 == 1
