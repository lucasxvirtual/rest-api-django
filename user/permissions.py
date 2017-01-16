from rest_framework import permissions                                                              

SAFE_METHODS = ['POST']

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):                                                        
        if(request.method in SAFE_METHODS):
            return True
        else:
            return request.user.is_authenticated()