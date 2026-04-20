from django.db import models
from accounts.models import CustomUserModel
# Create your models here.

class EmailLog(models.Model):
    Status_Choice=(
        ('sent','sent'),
        ('failed','failed')
    )
    user=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name='emails')
    subject=models.CharField(max_length=255)
    message=models.TextField()
    status=models.CharField(max_length=255 , choices=Status_Choice , default='sent')
    sent_at=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)



#   python manage.py makemigrations notification
#   python manage.py migrate
#   python manage.py runserver      