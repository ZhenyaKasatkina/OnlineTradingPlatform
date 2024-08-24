from django.db import models

NULLABLE = {"blank": True, "null": True}


class Participant(models.Model):
    """Участник торговой онлайн платформы"""

    name = models.CharField(max_length=150, verbose_name="Наименование")
    email = models.EmailField(
        verbose_name="Адрес электронной почты", unique=True
    )
    country = models.CharField(max_length=50, verbose_name="Страна")
    city = models.CharField(max_length=50, verbose_name="Город")
    street = models.CharField(max_length=50, verbose_name="Улица")
    house = models.CharField(max_length=10, verbose_name="Дом/строение")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )

    FACTORY = "завод"
    RETAIL_NETWORK = "розничная сеть"
    ENTREPRENEUR = "ИП"
    UNIT_NAME = {
        FACTORY: "завод",
        RETAIL_NETWORK: "розничная сеть",
        ENTREPRENEUR: "ИП",
    }
    unit_name = models.CharField(
        choices=UNIT_NAME,
        max_length=20,
        verbose_name="звено",
    )

    supplier = models.ForeignKey(
        "self",
        related_name="customer",
        verbose_name="поставщик",
        on_delete=models.SET_NULL,
        help_text="предыдущий по иерархии участник сети",
        parent_link=True,
        **NULLABLE,
    )

    debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    ZERO = "0"
    ONE = "1"
    TWO = "2"
    LEVEL = {
        ZERO: "0",
        ONE: "1",
        TWO: "2",
    }
    level = models.CharField(
        choices=LEVEL,
        max_length=3,
        verbose_name="уровень",
        **NULLABLE,
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.name}"

    class Meta:
        verbose_name = "участник"
        verbose_name_plural = "участники"
        # Сортировка по id
        ordering = ["-pk"]
