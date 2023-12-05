from rest_framework.permissions import BasePermission

class IsVerified(BasePermission): # custom permission to verified users
    def has_permission(self, request, view):
        return request.user.is_verified and request.user.is_authenticated
        
