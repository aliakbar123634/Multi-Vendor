from . models import Product , ProductImage , Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','slug','parent','is_active']
        read_only_fields=['id' ,'slug']        


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','shop' ,'category', 'name','slug' ,'description','price','discount_price','stock','is_available','sku' ,'weight','dimensions','views_count','is_featured','is_active','created_at']
        read_only_fields=['id' ,'slug','shop','views_count','is_active','created_at'] 

   # python manage.py runserver     