from django.db import models
from order.models import Order
import uuid
from vendor.models import VendorProfile
# Create your models here.
class Payment(models.Model):
    payment_choice=(
        ('stripe','stripe'),
        ('paypal' , 'paypal')
    )
    status_choice = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
    )     
    id=models.UUIDField(primary_key=True ,  default=uuid.uuid4 , editable=False)
    order=models.OneToOneField(Order , on_delete=models.CASCADE , related_name='payment')
    payment_method=models.CharField(max_length=255 , choices=payment_choice , default='stripe' ) 
    transaction_id=models.CharField(max_length=255 ,  unique=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency=models.CharField(max_length=255 ,  default='USD')
    status=models.CharField(max_length=255 , choices=status_choice , default='pending')
    paid_at=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)


class Payout(models.Model):
    status_choice = (
    ('pending', 'pending'),
    ('completed', 'completed'),
    ('failed', 'failed')
    )     
    vendor=models.ForeignKey(VendorProfile , on_delete=models.CASCADE , related_name='payouts')
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status=models.CharField(max_length=255 , choices=status_choice , default='pending')
    transaction_reference=models.CharField(max_length=255 , unique=True)
    paid_at=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)



#   python manage.py makemigrations payment
#   python manage.py migrate
#   python manage.py runserver