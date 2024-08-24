from django.contrib import admin
from relatives import RelativesAdmin

from participants.models import Participant


@admin.action(description="Очистить задолженность указанных поставщиков")
def is_clear_debt(modeladmin, request, queryset):
    for participants in queryset:
        participants.debt = 0.00
        participants.save()


@admin.register(Participant)
class ParticipantsAdmin(RelativesAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "level",
        "unit_name",
        "supplier",
        "debt",
        "created_at",
    )
    fields = [
        "name",
        (
            "email",
            "country",
            "city",
            "street",
            "house",
        ),
        (
            "level",
            "unit_name",
        ),
        (
            "supplier",
            "debt",
        ),
    ]
    list_filter = ("city",)
    actions = [is_clear_debt]
