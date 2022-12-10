from django.urls import reverse
from rest_framework import status, test

from Account.tests.criar_models import AccountUtils


class SerializersTests(test.APITestCase, AccountUtils):

    def get_jwt_token(self, username="testename", password="testesenha"):
        data = {
            "username": username,
            "password": password
        }

        token = self.client.post(reverse("Account:token"), data=data)
        return token.data["access"]

    # Account Serializer

    def test_validate_cpf_field(self):
        user = self.make_user()
        bank = self.make_bank()
        data = self.make_account_data(cpf="abcabcabcab", instituicao=bank.id)
        token = self.get_jwt_token()
        response = self.client.post(reverse("Account:list-account"), data=data, HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Users Serializer
    def test_validate_two_password_fields_are_not_equal(self):
        data = self.make_user_data(password2="outrasenha")
        response = self.client.post(reverse("Account:list-usuarios"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_two_password_fields_are_equal(self):
        data = self.make_user_data(password2="testesenha")
        response = self.client.post(reverse("Account:list-usuarios"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
