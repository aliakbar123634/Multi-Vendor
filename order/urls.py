from rest_framework.routers import DefaultRouter
from django.urls import path , include
from . import views
router=DefaultRouter()
router.register('cart' , views.CartViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('order/checkout/' , views.CreateOrderViewSet.as_view() , name="checkout" ),
    path('orders/' , views.OrderList.as_view() , name="orders"),
    path('orders/<uuid:id>/', views.SingleOrder.as_view(), name="order")
]




#     python manage.py runserver  