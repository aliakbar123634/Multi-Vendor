from django.db import models
from django.utils.text import slugify
from vendor.models import Shop
import uuid
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    is_active=models.BooleanField(default=True)
    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)    
    def __str__(self):
        return self.name     

class Product(models.Model):
    id=models.UUIDField(primary_key=True ,  default=uuid.uuid4 , editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category= models.ForeignKey(Category, on_delete=models.CASCADE , related_name='products')
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255, unique=True)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    sku = models.CharField(max_length=50, unique=True)
    weight = models.FloatField(blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    views_count = models.IntegerField(default=0)
    is_featured=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/',null=True, blank=True)
    alt_text=models.CharField(max_length=255)
    is_primary=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)





#   python manage.py makemigrations product
#   python manage.py migrate
#   python manage.py runserver    