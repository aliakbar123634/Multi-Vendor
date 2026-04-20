from django.shortcuts import render
from . models import VendorProfile , Shop
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from . serializers import VendorSerializer , ShopSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , AllowAny
from . permissions import VendorOnlyPermission , VendoritsOwnAndAdminEvery , VendoritsOwnAndAdminShop
from accounts.permissions import IsAdmin
from rest_framework.exceptions import ValidationError

# Create your views here.
class VendorViewSet(ModelViewSet):
    queryset=VendorProfile.objects.all()
    serializer_class=VendorSerializer
    def get_permissions(self):
        if self.action == "list":
            return [IsAdmin()]         
        if self.action == "create":
            return [VendorOnlyPermission()]  
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [VendoritsOwnAndAdminEvery()]              
        return super().get_permissions()
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'vendor_profile'):
            raise ValidationError("Vendor profile already exists")        
        serializer.save(user=self.request.user)


class ShopViewset(ModelViewSet):
    queryset=Shop.objects.all()
    serializer_class=ShopSerializer
    def get_permissions(self):
        if self.action == "create":
            return [VendorOnlyPermission()]  
        if self.action in ["update", "partial_update", "destroy"]:
            return [VendoritsOwnAndAdminShop()]  
        if self.action in ["retrieve", "list"]:   
            return [AllowAny()]           
        return super().get_permissions()
    @action(detail=False, methods=['get'], url_path='(?P<slug>[^/.]+)')
    def public_shop_detail(self, request, slug=None):
        try:
            shop = Shop.objects.get(slug=slug, is_active=True)
        except Shop.DoesNotExist:
            return Response(
                {"error": "Shop not found or inactive"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)



#  python manage.py runserver
