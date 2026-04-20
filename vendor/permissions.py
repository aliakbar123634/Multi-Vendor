from rest_framework.permissions import BasePermission

class VendorOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return (
            user and user.is_authenticated and user.role=="vendor"
        )


class VendoritsOwnAndAdminEvery(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return user and user.is_authenticated 
        
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if request.user.role == "vendor":
            return obj.user == request.user        
        return False
               

class VendoritsOwnAndAdminShop(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return user and user.is_authenticated 
        
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if request.user.role == "vendor":
            return obj.vendor.user == request.user        
        return False