from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):

    # native prebuilt method has_object
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
    # Basically owner in model is equal to authentiocated user then it return boolen true