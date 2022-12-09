from criar_models import AccountUtils
from django.urls import reverse
from rest_framework import status, test

from Account.models import Instituicao


class ContasTestes(test.APITestCase, AccountUtils):

    def get_jwt_token(self, username="testename", password="testesenha"):
        data = {
            "username": username,
            "password": password
        }

        token = self.client.post(reverse("Account:token"), data=data)
        return token.data["access"]

    # Admin User
    def test_admin_user_see_all_accounts(self):
        admin = self.make_user(is_staff=True)
        token = self.get_jwt_token()
        response = self.client.get(reverse("Account:list-account"), HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_change_all_accounts(self):
        admin = self.make_user(is_superuser=True)
        user = self.make_user(username="testename1", email="testemail@email.com")
        bank = self.make_bank()
        account = self.make_account(user, bank)
        token = self.get_jwt_token(username="testename", password="testesenha")
        data = self.make_account_data(nome="New Name", instituicao=bank.id)
        response = self.client.patch(reverse("Account:detail-account", kwargs={"pk": account.id}),
                                     data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_change_all_fields(self):
        admin = self.make_user(is_superuser=True)
        bank = self.make_bank()
        account = self.make_account(admin, bank)
        token = self.get_jwt_token(username="testename", password="testesenha")
        data = self.make_account_data(nome="New Name", instituicao=bank.id, cpf="93212343482", usuario=admin.id)
        response = self.client.put(reverse("Account:detail-account", kwargs={"pk": account.id}),
                                     data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Not authenticated User
    def test_user_not_authenticated_is_unauthorized(self):
        response = self.client.get(reverse("Account:list-account"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_user_cant_create_account(self):
        bank = self.make_bank()
        data = self.make_account_data(instituicao=bank.id)
        response = self.client.post(reverse("Account:list-account"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Authenticated User
    def test_user_authenticated_is_unauthorized_to_see_all_accounts(self):
        user = self.make_user()
        token = self.get_jwt_token()
        response = self.client.get(reverse("Account:list-account"), data={"HTTP_Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_authenticated_see_just_your_account(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(usuario=user, instituicao=bank)
        response = self.client.get(reverse("Account:detail-account", kwargs={"pk": account.id}), HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.data["id"], account.id)

    def test_user_authenticated_dont_see_other_account(self):
        user1, user2 = self.make_user(username="testeuser1", email="teste1@email.com"), self.make_user(username="testeuser2", email="teste2@email.com")
        bank = self.make_bank()
        account_user2 = self.make_account(user2, cpf="12332132112", instituicao=bank)
        token_user1 = self.get_jwt_token(username="testeuser1", password="testesenha")
        response = self.client.get(reverse("Account:detail-account", kwargs={"pk": account_user2.id}), HTTP_AUTHORIZATION=f"Bearer {token_user1}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_your_account(self):
        user = self.make_user()
        bank = self.make_bank()
        token = self.get_jwt_token()
        data = self.make_account_data(instituicao=bank.id)
        response = self.client.post(reverse("Account:list-account"), data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_create_just_one_accont(self):
        user = self.make_user()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        token = self.get_jwt_token()
        data = self.make_account_data(instituicao=bank.id)
        response = self.client.post(reverse("Account:list-account"), data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_cant_patch_change_your_account_name(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        data = {"nome": "TestePatch"}
        response = self.client.patch(reverse("Account:detail-account", kwargs={"pk": account.id}),
                                     data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cant_patch_add_money(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        data = {"saldo": "123.0"}
        response = self.client.patch(reverse("Account:detail-account", kwargs={"pk": account.id}),
                                     data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cant_patch_change_your_account_cpf(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        data = {"cpf": "12332112344"}
        response = self.client.patch(reverse("Account:detail-account", kwargs={"pk": account.id}),
                                     data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cant_patch_change_bank(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank1, bank2 = self.make_bank(), self.make_bank(nome_instituicao="bradesco")
        account = self.make_account(user, instituicao=bank1)
        data = {"instituicao": f"{bank2.id}"}
        response = self.client.patch(
            reverse("Account:detail-account", kwargs={"pk": account.id}),
            data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_put_change_your_account_name(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        data = self.make_account_data(instituicao=bank.id, usuario=user.id)
        response = self.client.put(reverse("Account:detail-account", kwargs={"pk": account.id}),
                                   data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cant_put_change_other_accont(self):
        user1, user2 = self.make_user(username="testeuser1", email="teste1@email.com"), self.make_user(username="testeuser2", email="teste2@email.com")
        token = self.get_jwt_token(username="testeuser1", password="testesenha")
        bank = self.make_bank()
        account_user2 = self.make_account(user2, cpf="12332132112", instituicao=bank)
        data = self.make_account_data(cpf="12332132112", instituicao=bank.id, usuario=user2.id)
        response = self.client.put(reverse("Account:detail-account", kwargs={"pk": account_user2.id}),
                                   data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_cant_put_change_your_account_cpf(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        data = self.make_account_data(cpf="12333342122", instituicao=bank.id, usuario=user.id)
        response = self.client.put(reverse("Account:detail-account", kwargs={"pk": account.id}), data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cant_put_add_money(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        data = self.make_account_data(instituicao=bank.id, usuario=user.id, saldo="321321.0")
        response = self.client.put(reverse("Account:detail-account", kwargs={"pk": account.id}), data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.data["saldo"], account.saldo)

    def test_authenticated_user_can_delete_your_account(self):
        user = self.make_user()
        token = self.get_jwt_token()
        bank = self.make_bank()
        account = self.make_account(user, instituicao=bank)
        response = self.client.delete(reverse("Account:detail-account", kwargs={"pk": account.id}), HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_user_cant_delete_other_accont(self):
        user1, user2 = self.make_user(username="testeuser1", email="teste1@email.com"), self.make_user(username="testeuser2", email="teste2@email.com")
        token = self.get_jwt_token(username="testeuser1", password="testesenha")
        bank = self.make_bank()
        account_user2 = self.make_account(user2, cpf="12332132112", instituicao=bank)
        response = self.client.delete(reverse("Account:detail-account", kwargs={"pk": account_user2.id}), HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)