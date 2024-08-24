from django.urls import reverse
from django.utils import translation
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from participants.models import Participant
from users.models import User


class ParticipantTestCase(APITestCase):
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

    def test_participant_create_is_true(self):
        """Проверка создания участника платформы (без ошибки)"""

        url = reverse("participants:create")
        data = {
            "name": "ПАО Посредник",
            "email": "PPP@list.ru",
            "country": "Россия",
            "city": "Москва",
            "street": "Московская",
            "house": "5",
            "unit_name": "ИП",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participant.objects.all().count(), 2)

    def test_participant_create_is_false(self):
        """Проверка создания участника платформы (с ошибкой)"""

        url = reverse("participants:create")
        data = {
            "email": "PPP@list.ru",
            "country": "Россия",
            "city": "Москва",
            "street": "Московская",
            "house": "5",
            "unit_name": "ИП",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Participant.objects.all().count(), 1)

    def test_participant_update_is_true(self):
        """Проверка изменения участника платформы
        (без ошибки, изменилось название страны)"""

        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Россия",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "завод",
            "level": "0",
            "supplier": "",
            "debt": "0.00",
        }

        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("country"), data["country"])

    def test_participant_update_is_false_not_email(self):
        """Проверка изменения участника платформы
        (с ошибкой, email не меняется)"""

        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "null",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "завод",
            "level": "0",
            "supplier": "",
            "debt": "0.00",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.get("email"), ["Enter a valid email address."])

    def test_participant_update_is_false_level(self):
        """Проверка изменения участника платформы
        (с ошибкой, завод может быть только с уровнем 0)"""

        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "завод",
            "level": "2",
            "supplier": "",
            "debt": "0.00",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {"non_field_errors": ["Завод всегда находится на нулевом(0) уровне."]},
        )

    def test_participant_update_is_false_unit_name_and_level(self):
        """Проверка изменения участника платформы
        (с ошибкой, ИП и розничная сеть только на 1 и 2 уровнях)"""

        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "розничная сеть",
            "level": "0",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {
                "non_field_errors": [
                    "'Розничная сеть' и 'ИП' могут быть только на 1-м или 2-м уровне."
                ]
            },
        )

    def test_participant_update_is_false_supplier_and_level(self):
        """Проверка изменения участника платформы
        (с ошибкой, если есть поставщик то уровень должен быть 1 или 2.)"""

        participant = Participant.objects.create(
            name="ПАО Посредник",
            email="PPP@list.ru",
            country="Россия",
            city="Москва",
            street="Московская",
            house="5",
            unit_name="завод",
            level="0",
        )
        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "завод",
            "level": "0",
            "supplier": participant.pk,
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {
                "non_field_errors": [
                    "Если есть поставщик то Ваш уровень должен быть '1' или '2'."
                ]
            },
        )

    def test_participant_update_is_false_supplier_and_buyer(self):
        """Проверка изменения участника платформы
        (с ошибкой, поставщик и покупатель не могут быть одним лицом)"""

        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "ИП",
            "level": "1",
            "supplier": self.participant.pk,
            "debt": "0.00",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {"non_field_errors": ["Покупатель и поставщик не могут быть одним лицом."]},
        )

    def test_participant_update_is_false_supplier_level_0(self):
        """Проверка изменения участника платформы
        (с ошибкой, если поставщик с уровнем 0 покупатель должен быть 1.)"""

        participant = Participant.objects.create(
            name="ПАО Завод",
            email="PPP@list.ru",
            country="Россия",
            city="Москва",
            street="Московская",
            house="5",
            unit_name="завод",
            level="0",
        )
        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "ИП",
            "level": "2",
            "supplier": participant.pk,
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {
                "non_field_errors": [
                    "Вы выбрали поставщика с уровнем '0', Ваш уровень должен быть '1'."
                ]
            },
        )

    def test_participant_update_is_false_supplier_level_1(self):
        """Проверка изменения участника платформы
        (с ошибкой, если поставщик с уровнем 0 покупатель должен быть 1.)"""

        participant = Participant.objects.create(
            name="ПАО розничная сеть",
            email="PPP@list.ru",
            country="Россия",
            city="Москва",
            street="Московская",
            house="5",
            unit_name="розничная сеть",
            level="1",
        )
        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "ИП",
            "level": "1",
            "supplier": participant.pk,
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {
                "non_field_errors": [
                    "Вы выбрали поставщика с уровнем '1', Ваш уровень должен быть '2'."
                ]
            },
        )

    def test_participant_update_is_false_supplier_level_2(self):
        """Проверка изменения участника платформы
        (с ошибкой, если поставщик с уровнем 0 покупатель должен быть 1.)"""

        participant = Participant.objects.create(
            name="ПАО розничная сеть",
            email="PPP@list.ru",
            country="Россия",
            city="Москва",
            street="Московская",
            house="5",
            unit_name="розничная сеть",
            level="2",
        )
        url = reverse("participants:update", args=(self.participant.pk,))
        data = {
            "id": self.participant.pk,
            "name": "ООО Мир",
            "email": "vvv@list.ru",
            "country": "Другая",
            "city": "N",
            "street": "New",
            "house": "36/5",
            "unit_name": "ИП",
            "level": "2",
            "supplier": participant.pk,
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            {"non_field_errors": ["Поставщик с уровнем '2' не осуществляет поставки."]},
        )

    def test_participant_delete_is_true(self):
        """Проверка удаления участника платформы
        (без ошибки)"""

        url = reverse("participants:delete", args=(self.participant.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Participant.objects.all().count(), 0)

    def test_participant_delete_is_false_not_is_staff(self):
        """Проверка удаления участника платформы (с ошибкой, нет доступа)"""

        self.user.is_staff = False
        url = reverse("participants:delete", args=(self.participant.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Participant.objects.all().count(), 1)

    def test_participant_delete_is_false(self):
        """Проверка удаления участника платформы
        (с ошибкой, нет такого участника)"""

        url = reverse("participants:delete", args=(101,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Participant.objects.all().count(), 1)

    def test_participant_list_is_true(self):
        """Проверка списка участников платформы"""

        url = reverse("participants:list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.participant.pk,
                "name": "ООО Мир",
                "email": "vvv@list.ru",
                "country": "Другая",
                "city": "N",
                "street": "New",
                "house": "36/5",
                "unit_name": "завод",
                "level": "0",
                "supplier": None,
                "debt": "0.00",
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_participant_list_is_false(self):
        """Проверка списка участников (нет доступа)"""

        self.user.employer = None
        url = reverse("participants:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)
        super().tearDown()
