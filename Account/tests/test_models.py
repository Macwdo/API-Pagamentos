from criar_models import AccountUtils
from rest_framework import test


class TabelasTestes(test.APITestCase, AccountUtils):

    def test_instituicao_retorna_banco(self):
        instituicao = self.make_bank()
        self.assertEqual(str(instituicao), instituicao.nome_instituicao)

    def test_conta_retorna_nome_da_conta(self):
        usuario = self.make_user()
        banco = self.make_bank()
        conta = self.make_account(usuario=usuario, instituicao=banco)
        self.assertEqual(str(conta), conta.nome)

    def test_transferencia_retorna_origem_nome(self):
        usuario = self.make_user()
        banco = self.make_bank()
        conta = self.make_account(usuario=usuario, instituicao=banco)
        transferencia = self.make_transfer(origem=conta)
        self.assertEqual(str(transferencia), transferencia.origem.nome)