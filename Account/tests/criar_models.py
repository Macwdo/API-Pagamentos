from django.contrib.auth.models import User
from rest_framework.test import APISimpleTestCase
from Account.models import Conta, Instituicao, Transferencia


class AccountUtils(APISimpleTestCase):

    CPF = "12345678900"


    def make_user(
        self,
        username="testename",
        email="teste@email.com",
        password="testesenha",
        **kwargs
    ):
        usuario = User.objects.create(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def make_user_data(
        self,
        username="testename",
        email="teste@email.com",
        password="testesenha",
        **kwargs
    ):  
        data = {
            "username": username,
            "email": email,
            "password": password,
        }
        if kwargs:
            for key, values in kwargs.items():
                data[key] = values
        return data


    def make_bank(
        self,
        nome_instituicao="Itau"
    ):
        instituicao = Instituicao.objects.create(
            nome_instituicao=nome_instituicao
        )

        return instituicao

    def make_bank_data(
        self,
        nome_instituicao="Itau"
    ):
        data = {
            "nome_instituicao": nome_instituicao
        }

        return data


    def make_account(
        self,
        usuario=None,
        instituicao=None,
        nome="Teste teste",
        saldo=0.0,
        cpf=None
    ):
        if not cpf:
            cpf = self.CPF

        if not usuario:
            usuario = {}


        conta = Conta.objects.create(
            usuario=usuario,
            nome=nome,
            cpf=cpf,
            saldo=saldo,
            instituicao=instituicao
        )
        return conta

    def make_account_data(
        self,
        instituicao=None,
        nome="Teste Account",
        cpf=None,
        **kwargs
    ):
        if not cpf:
            cpf = self.CPF

        data = {
            "nome": nome,
            "cpf": cpf,
            "instituicao": instituicao
        }

        if kwargs:
            for key, values in kwargs.items():
                data[key] = values
        return data

    def make_transfer(
        self,
        origem=None,
        valor=10

    ):
        if not origem:
            origem = {}

        transferencia = Transferencia.objects.create(
            origem=origem,
            destino=self.CPF,
            valor=valor
        )
        return transferencia

    # def get_jwt_token(username, password):
    #     ...
