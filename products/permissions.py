from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Сотрудник владельца продукта
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user.employer:
            return True
        return False
