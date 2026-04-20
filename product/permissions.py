from rest_framework.permissions import BasePermission

class VendoerOwnProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if request.user.role == "vendor":
            return obj.shop.vendor.user == request.user        
        return False        


class AdminandVendorWithprofile(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        # Vendor must have shop
        if user.role == "vendor":
            return hasattr(user, "vendor_profile") and hasattr(user.vendor_profile, "shop")

        return False