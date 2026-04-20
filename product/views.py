from django.shortcuts import render
from . models import *
from . serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.permissions import IsAdmin
from product.permissions import VendoerOwnProduct , AdminandVendorWithprofile
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAdmin]
    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]        
        return super().get_permissions()
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[VendoerOwnProduct]
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(
            shop=user.vendor_profile.shop
        )
    def get_permissions(self):
        if self.action == "create":
            return [AdminandVendorWithprofile()]   
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]               
        return super().get_permissions()
    # @action(detail=False, methods=['get'], url_path='(?P<slug>[^/.]+)')
    # def product_detail(self, request, slug=None):
    #     try:
    #         product=Product.objects.get(slug=slug, is_active=True ,is_available=True )
    #     except Product.DoesNotExist:
    #         return Response(
    #             {"error": "Product not found or inactive or not available"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )                
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data, status=status.HTTP_200_OK)    

#    python manage.py runserver    