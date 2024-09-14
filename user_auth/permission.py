from rest_framework.permissions import BasePermission


class IsWarehouseUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return (
            request.user
            and hasattr(request.user, "role")
            and request.user.role == "warehouse"
            and request.user.is_staff
        )


class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user and hasattr(request.user, "role") and request.user.role == "client"


class IsCourierUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user and hasattr(request.user, "role") and request.user.role == "courier"
