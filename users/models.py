from django.contrib.auth.models import AbstractUser
from django.db import models

from participants.models import Participant

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    last_name = models.CharField(max_length=50, verbose_name="фамилия")
    first_name = models.CharField(max_length=50, verbose_name="имя")
    employer = models.ForeignKey(
        Participant,
        related_name="user",
        verbose_name="работодатель",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
