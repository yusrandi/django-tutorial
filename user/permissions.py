from rest_framework.permissions import BasePermission


class IsAuthenticatedNonStaff(BasePermission):
    """Allow access only to authenticated users who are not staff."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff == True
        )
