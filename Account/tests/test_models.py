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

    def test_transferencia_retorna_nome(self):
        origem, destino = self.make_user(), self.make_user(username="testename2", email="teste2@email.com")
        banco = self.make_bank()
        conta_origem, conta_destino = self.make_account(usuario=origem, instituicao=banco), self.make_account(usuario=destino, instituicao=banco, cpf="99211299932")
        transferencia = self.make_transfer(origem=conta_origem, destino=conta_destino)
        self.assertEqual(str(transferencia), f"{conta_origem.nome} - {conta_destino.nome}")