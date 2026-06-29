from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    message = 'Access restricted to Admin users only.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsLecturer(BasePermission):
    message = 'Access restricted to Lecturer users only.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'lecturer'
        )


class IsStudent(BasePermission):
    message = 'Access restricted to Student users only.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'student'
        )


class IsAdminOrLecturer(BasePermission):
    message = 'Access restricted to Admin or Lecturer users.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ('admin', 'lecturer')
        )


class IsAdminOrReadOnly(BasePermission):
    """Admin can write; anyone can read (AllowAny for GET)."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )