from rest_framework import permissions

# Shared method
def is_active_and_role(user, expected_role):
    return user.is_authenticated and user.is_active and user.role == expected_role

class IsTechAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_active_and_role(request.user, 'tech-admin')

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_active_and_role(request.user, 'manager')

class IsCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_active_and_role(request.user, 'cashier')

class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_active_and_role(request.user, 'agent')
