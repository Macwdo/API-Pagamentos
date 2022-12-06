from Account.models import Transferencia, Conta, Instituicao
from django.contrib.auth.models import User


class AccountUtils:

    CPF = "12345678900"

    def make_usuario(
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

    def make_instituicao(
        self,
        nome_instituicao="Itau"
    ):
        instituicao = Instituicao.objects.create(
            nome_instituicao=nome_instituicao
        )

        return instituicao

    def make_conta(
        self,
        usuario=None,
        instituicao=None,
        nome="Teste teste",
        saldo=0.0,
    ):
        if not usuario:
            usuario = {}
        
        if not instituicao:
            instituicao = {}

        conta = Conta.objects.create(
            usuario=usuario,
            nome=nome,
            cpf=self.CPF,
            saldo=saldo,
            instituicao=Instituicao.objects.create(**instituicao)
        )
        return conta

    def make_transferencia(
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

