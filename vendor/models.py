from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUserModel
# Create your models here.

class VendorProfile(models.Model):
    user=models.OneToOneField(CustomUserModel , on_delete=models.CASCADE , related_name='vendor_profile')
    business_name=models.CharField(max_length=255)
    business_email=models.EmailField(max_length=15, unique=True)
    business_phone=models.CharField(max_length=15)
    cnic_number=models.CharField(max_length=30)
    tax_number = models.CharField(max_length=30, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    rating=models.FloatField(default=0)
    total_earnings=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.business_name
    


class Shop(models.Model):
    vendor=models.OneToOneField(VendorProfile ,on_delete=models.CASCADE , related_name='shop' )    
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255, unique=True)
    description=models.TextField()
    logo=models.ImageField(upload_to='shop/logo/', blank=True, null=True)
    banner=models.ImageField(upload_to='shop/banner/', blank=True, null=True)
    address=models.TextField()
    city=models.CharField(max_length=15)
    country=models.CharField(max_length=15)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)    
    def __str__(self):
        return self.name        
    



#  python manage.py makemigrations vendor
#  python manage.py migrate
#  python manage.py runserver