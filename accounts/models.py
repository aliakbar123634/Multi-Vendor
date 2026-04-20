from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser , BaseUserManager 
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required ...")
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUserModel(AbstractUser):
    role=(
        ('buyer' , 'buyer'),
        ('vendor' , 'vendor'),
        ('admin' , 'admin')
    )    
    id=models.UUIDField(primary_key=True ,  default=uuid.uuid4 , editable=False)
    email=models.EmailField(unique=True)
    full_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15 , blank=True, null=True)
    role=models.CharField(max_length=30 , choices=role, default='buyer')
    is_verified = models.BooleanField(default=False , null=True , blank=True)
    profile_image = models.ImageField(upload_to='profile_images/',null=True, blank=True)
    address=models.TextField(blank=True, null=True)
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []    
    objects=CustomUserManager()
    def __str__(self):
        return self.email
    





#  python manage.py createsuperuser  
#  python manage.py runserver   