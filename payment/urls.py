from django.urls import path
from . import views 
urlpatterns = [
    path('create-intent/', views.CreatePaymentIntentAPIView.as_view() , name="create-intent"),
    path('webhook/', views.StripeWebhookAPIView.as_view() , name="webhook"),
]
#   python manage.py runserver