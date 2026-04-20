from rest_framework.permissions import BasePermission

class BuyerOnly(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return (
            user and user.is_authenticated and user.role=="buyer"
        )

class BayerOwnCart(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role != "buyer":
            return False
        return obj.cart.user == user
    
class IsOrderOwnerOrVendorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'buyer':
            return obj.user == user
        if user.role == 'vendor':
            return obj.orderitems.filter(
                vendor=user.vendor_profile
            ).exists()
        return False    
    
    