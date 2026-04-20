from rest_framework.routers import DefaultRouter
from django.urls import path , include
from . import views
router=DefaultRouter()
router.register('products' , views.ProductViewSet)
router.register('category' , views.CategoryViewSet , basename='categoryOfProduct')
urlpatterns = [
    path('' , include(router.urls))
]



#    python manage.py runserver