from . serializers import *
from . models import *
from rest_framework.viewsets import ModelViewSet
from . permissins import BuyerOnly , BayerOwnCart , IsOrderOwnerOrVendorOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from decimal import Decimal
# Create your views here.


class CartViewSet(ModelViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[AllowAny]
    def get_permissions(self):
        if self.action in ["create", "list" , "destroy"]: 
            return [BuyerOnly()]         
        return super().get_permissions()

    @action(detail=False, methods=['PUT', 'PATCH'], url_path='item/(?P<item_id>[^/.]+)')
    def item_detail(self, request, item_id=None):
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Not your cart item")
        ser = CartItemSerializer(instance=cart_item,data=request.data,partial=True ) 
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['DELETE'], url_path='item/(?P<item_id>[^/.]+)' , permission_classes=[BayerOwnCart])
    def delete_item(self, request, item_id=None):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return Response(
            {"message":"Cart Item delete successfully  ....."},status=status.HTTP_200_OK
        )   


class CreateOrderViewSet(APIView):
    permission_classes=[BuyerOnly]
    def post(self , request):
        user=request.user
        try:
            cart_of_id=Cart.objects.get(user=user, is_active=True)
        except Cart.DoesNotExist:
            return Response({
                "message":"Cart does not exists at given id"
            }, status=status.HTTP_400_BAD_REQUEST)   
        cart_items_related_to_cart=cart_of_id.cartitems.all()
        if not cart_items_related_to_cart.exists():
            return Response({"Order Cart is empty .........."},status=400)
        with transaction.atomic():
            total=0
            cr_order=Order.objects.create(
                user=user,
                shipping_address=request.data.get("shipping_address"),
                billing_address=request.data.get("billing_address"),
                status="pending",
                payment_status="pending"
            )
            for i in cart_items_related_to_cart:
                # price=i.price
                price = i.product.price
                commission_amount=price * Decimal('0.05')
                vendor_earning=price-commission_amount
                total+=price * i.quantity
                OrderItem.objects.create(
                    order=cr_order,
                    product=i.product,
                    vendor=i.product.shop.vendor,
                    quantity=i.quantity,
                    price=price,
                    commission_amount=commission_amount,
                    vendor_earning=vendor_earning
                )   
            shipping_fee=200
            tax_amount=total * Decimal('0.05')
            grand_total = total + shipping_fee + tax_amount
            cr_order.shipping_fee=shipping_fee
            cr_order.tax_amount=tax_amount
            cr_order.total_amount=grand_total
            cr_order.save()
        serializer = OrderSerializer(cr_order)
        return Response(serializer.data, status=status.HTTP_200_OK)    
   
class OrderList(APIView):
    permission_classes=[IsOrderOwnerOrVendorOrAdmin]
    def get(self , request):
        user=request.user
        order=Order.objects.filter(user=user)
        if not order.exists():
            return Response({"Order list is empty .........."},status=400)
        ser=OrderSerializer(order ,many=True)
        return Response(ser.data, status=status.HTTP_200_OK)    
class SingleOrder(APIView):
    permission_classes=[IsOrderOwnerOrVendorOrAdmin]
    def get(self , request, id):
        user=request.user
        try:
            order=Order.objects.get(user=user, id=id)
        except Order.DoesNotExist():
            return Response({"Given UUID id wrong .........."},status=400)
        ser=OrderSerializer(order)
        return Response(ser.data, status=status.HTTP_200_OK)      




#     python manage.py runserver    