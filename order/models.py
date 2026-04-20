from django.db import models
from accounts.models import CustomUserModel
from product.models import Product
from vendor.models import VendorProfile
import uuid
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name='carts' )
    total_price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart , on_delete=models.CASCADE , related_name='cartitems')   
    product=models.ForeignKey(Product , on_delete=models.CASCADE , related_name='cartitems') 
    quantity=models.IntegerField()  
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    created_at=models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    status_choice=(
        ('pending' , 'pending'),
        ('paid' , 'paid'),
        ('shipped' , 'shipped'),
        ('delivered' , 'delivered'),
        ('cancelled' , 'cancelled')
    ) 
    payment_status_choices = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
    )     
    id=models.UUIDField(primary_key=True ,  default=uuid.uuid4 , editable=False)
    user=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE ,related_name="orders")
    status=models.CharField(max_length=255 , choices=status_choice , default='pending')
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    shipping_fee=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=50, choices=payment_status_choices, default='pending')
    shipping_address=models.TextField()
    billing_address=models.TextField()
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    ordered_at=models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order=models.ForeignKey(Order , on_delete= models.CASCADE , related_name='orderitems')
    product=models.ForeignKey(Product , on_delete=models.CASCADE , related_name='orderitems')
    vendor=models.ForeignKey(VendorProfile , on_delete=models.CASCADE , related_name='orderitems')
    quantity=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor_earning=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at=models.DateTimeField(auto_now_add=True)




#   python manage.py makemigrations order
#   python manage.py migrate
#   python manage.py runserver      