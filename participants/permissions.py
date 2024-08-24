from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """
    Активный сотрудник
    """

    def has_permission(self, request, view):
        if request.user.employer:
            return True
        return False
