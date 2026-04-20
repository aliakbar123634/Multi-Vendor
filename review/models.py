from django.db import models
from accounts.models import CustomUserModel
from product.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Review(models.Model):
    user=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name='reviews')
    product=models.ForeignKey(Product , on_delete=models.CASCADE , related_name='review')
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment=models.TextField(blank=True, null=True)
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'product']


#   python manage.py makemigrations review
#   python manage.py migrate
#   python manage.py runserver         