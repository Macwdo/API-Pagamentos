from criar_models import AccountUtils
from rest_framework import test


class TabelasTestes(test.APITestCase, AccountUtils):
    

    def test_instituicao_retorna_banco(self):
        instituicao = self.make_instituicao()
        self.assertEqual(str(instituicao), instituicao.nome_instituicao)

    def test_conta_retorna_nome_da_conta(self):
        usuario = self.make_usuario()
        conta = self.make_conta(usuario=usuario)
        self.assertEqual(str(conta), conta.nome)
    
    def test_transferencia_retorna_origem_nome(self):
        usuario = self.make_usuario()
        conta = self.make_conta(usuario=usuario)
        transferencia = self.make_transferencia(origem=conta)
        self.assertEqual(str(transferencia), transferencia.origem.nome)