from django.db import models

from participants.models import Participant

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    """Продукты"""

    product_name = models.CharField(max_length=150, verbose_name="наименование")
    model = models.CharField(max_length=50, verbose_name="модель")
    release_date = models.DateField(verbose_name="Дата выхода продукта")
    owner = models.ForeignKey(
        Participant,
        related_name="product",
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"{self.product_name}, модель: {self.model} "
            f"(дата выхода продукта на рынок: {self.release_date})"
        )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
