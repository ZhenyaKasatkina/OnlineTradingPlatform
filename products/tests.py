from django.urls import reverse
from django.utils import translation
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from participants.models import Participant
from products.models import Product
from users.models import User


class ProductTestCase(APITestCase):
    def setUp(self) -> None:

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
            employer=self.participant,
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            product_name="телефон",
            model="sony",
            release_date="2020-01-28",
            owner=self.participant,
        )

    def test_product_create_is_true(self):
        """Проверка создания продукта (без ошибки)"""

        url = reverse("products:create")
        data = {
            "product_name": "телефон",
            "model": "super sony",
            "release_date": "2021-01-28",
            "owner": self.participant.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_create_is_false_no_access(self):
        """Проверка создания продукта (с ошибкой)"""

        self.user.employer = None
        url = reverse("products:create")
        data = {
            "product_name": "телефон",
            "model": "super sony",
            "release_date": "2021-01-28",
            "owner": self.participant.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_product_create_is_false(self):
        """Проверка создания продукта (с ошибкой)"""

        url = reverse("products:create")
        data = {
            "model": "super sony",
            "release_date": "2021-01-28",
            "owner": self.participant.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_product_update_is_true(self):
        """Проверка изменения продукта
        (без ошибки, изменилось название модели)"""

        url = reverse("products:update", args=(self.product.pk,))
        data = {
            "id": self.participant.pk,
            "product_name": "телефон",
            "model": "super sony",
            "release_date": "2021-01-28",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("model"), data["model"])

    def test_product_update_is_false(self):
        """Проверка изменения продукта
        (с ошибкой)"""

        self.user.employer = None
        url = reverse("products:update", args=(self.product.pk,))
        data = {
            "id": self.participant.pk,
            "product_name": "телефон",
            "model": "sony",
            "release_date": "2020-01-28",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(result, {"detail": "No Product matches the given query."})

    def test_participant_delete_is_true(self):
        """Проверка удаления продукта
        (без ошибки)"""

        url = reverse("products:delete", args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_product_delete_is_false_not_employer(self):
        """Проверка удаления участника платформы
        (с ошибкой, нет у пользователя такого продукта)"""

        self.user.employer = None
        url = reverse("products:delete", args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_product_delete_is_false(self):
        """Проверка удаления продукта
        (с ошибкой, нет такого продукта)"""

        url = reverse("products:delete", args=(101,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_product_list_is_true(self):
        """Проверка списка продуктов"""

        url = reverse("products:list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.product.pk,
                "product_name": "телефон",
                "model": "sony",
                "release_date": "2020-01-28",
                "owner": self.participant.pk,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_product_list_is_false(self):
        """Проверка списка продуктов (нет доступа)"""

        self.user.employer = None
        url = reverse("products:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_retrieve_is_true(self):
        """Просмотр продукта"""

        url = reverse("products:view", args=(self.product.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            "id": self.product.pk,
            "product_name": "телефон",
            "model": "sony",
            "release_date": "2020-01-28",
            "owner": self.participant.pk,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_product_retrieve_is_false(self):
        """Просмотр продукта (с ошибкой)"""

        self.user.employer = None
        url = reverse("products:view", args=(1002,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)
        super().tearDown()
