import os

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from participants.models import Participant
from users.models import User

ROOT_DIR = os.path.dirname(__file__)


class UsersTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.participant = Participant.objects.create(
            name="ООО Мир",
            email="vvv@list.ru",
            country="Другая",
            city="N",
            street="New",
            house="36/5",
            unit_name="завод",
            level="0",
        )

        self.user = User.objects.create(
            email="vvv@list.ru",
            last_name="Иванов",
            first_name="Иван",
            password=make_password("123qwe"),
            employer=self.participant,
            is_staff=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_login_is_true(self):
        """Проверка login (без ошибки)"""

        url = reverse("users:login")
        data = {"email": "vvv@list.ru", "password": "123qwe"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_is_false_password(self):
        """Проверка login (с ошибкой, пароль)"""

        url = reverse("users:login")

        data = {"email": "vvv@list.ru", "password": "1q"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_is_false_email(self):
        """Проверка login (с ошибкой, email)"""

        url = reverse("users:login")
        data = {"email": "123asd", "password": "123qwe"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_is_true(self):
        """Проверка создания пользователя"""

        url = reverse("users:create")
        data = {
            "email": "create@list.ru",
            "password": "qwe",
            "last_name": "Сидоров",
            "first_name": "Петр",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_create_is_false(self):
        """Проверка создания пользователя (с ошибкой)"""

        url = reverse("users:create")
        data = {"email": "create@list.ru"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 1)

    def test_update_is_true(self):
        """Проверка изменения пользователя"""

        user = User.objects.create(
            email="new@list.ru",
            password=make_password("123qwe"),
            last_name="Синицина",
            first_name="Галина",
        )
        url = reverse("users:update", args=(user.pk,))
        data = {
            "email": "new@list.ru",
            "last_name": "Синицина",
            "first_name": "Галина",
            "password": "123qwe",
            "employer": self.participant.pk,
        }
        response = self.client.put(url, data)
        data = response.json()
        result = {
            "id": user.pk,
            "email": "new@list.ru",
            "last_name": "Синицина",
            "first_name": "Галина",
            "employer": self.participant.pk,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_update_false_no_access(self):
        """Проверка изменения пользователя
        (с ошибкой, нет доступа"""

        user = User.objects.create(
            email="new@list.ru",
            password=make_password("123qwe"),
            last_name="Синицина",
            first_name="Галина",
        )
        self.user.is_staff = False
        url = reverse("users:update", args=(user.pk,))
        data = {
            "email": "new@list.ru",
            "last_name": "Синицина",
            "first_name": "Галина",
            "password": "123qwe",
            "employer": self.participant.pk,
        }
        response = self.client.put(url, data)
        data = response.json()
        result = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data, result)

    def test_update_is_false(self):
        """Проверка изменения пользователя (с ошибкой)"""

        url = reverse("users:update", args=(102,))
        data = {"email": "vvv@list.ru", "employer": self.participant.pk}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No User matches the given query."}
        )

    def test_delete_is_true(self):
        """Проверка удаления пользователя (без ошибки)"""

        url = reverse("users:delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_delete_is_false(self):
        """Проверка удаления пользователя (с ошибкой)"""

        url = reverse("users:delete", args=(103,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.all().count(), 1)

    def test_delete_is_false_no_access(self):
        """Проверка удаления пользователя (с ошибкой, нет доступа)"""

        self.user.is_staff = False
        url = reverse("users:delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.all().count(), 1)
