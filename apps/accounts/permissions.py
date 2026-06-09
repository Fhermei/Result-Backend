from rest_framework.permissions import BasePermission


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
    message = 'Write access restricted to Admin users.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.role == 'admin'