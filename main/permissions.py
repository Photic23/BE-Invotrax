from rest_framework import permissions
from rolepermissions.checkers import has_permission, has_role

class HasRolePermission(permissions.BasePermission):
    """
    Permission class to check if user has the required permission
    """
    def has_permission(self, request, view):
        permission_name = getattr(view, 'required_permission', None)
        
        if not permission_name:
            return True
            
        return has_permission(request.user, permission_name)