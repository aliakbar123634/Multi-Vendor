from rest_framework import serializers
from . models import Order , OrderItem , Cart , CartItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product','vendor', 'quantity','price','commission_amount','vendor_earning']  
        read_only_fields = ['price', 'commission_amount', 'vendor_earning']
class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','user','status','payment_status','total_amount','shipping_fee','tax_amount','shipping_address','billing_address','tracking_number','ordered_at','orderitems']
        read_only_fields = ['user', 'status', 'payment_status', 'total_amount']
    


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','user', 'total_price', 'is_active', 'created_at']
        read_only_fields=['id' ,'user','created_at']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','cart', 'product', 'quantity', 'price', 'created_at']
        read_only_fields=['id','created_at']




#     python manage.py runserver