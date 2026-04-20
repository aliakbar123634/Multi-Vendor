from rest_framework import serializers
from . models import VendorProfile , Shop

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorProfile
        fields=['id','business_name','business_email','cnic_number','tax_number','is_verified','rating','total_earnings','available_balance','created_at']
        read_only_fields=['id' ,'is_verified','rating','total_earnings','available_balance','created_at']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields=['id','vendor','name','slug','description','logo','banner','address','city','country','is_active','created_at']
        read_only_fields=['id' ,'slug','created_at']


#   python manage.py runserver