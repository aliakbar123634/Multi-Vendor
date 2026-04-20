from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('auth/register/', views.ResgisterationView , name='register'),
    path('auth/login/', views.LoginSerializer , name='login'),
    path('auth/logout/', views.LogOutView , name='logout'),
    path('auth/profile/', views.allUserProfile , name='profile'),
    # path('auth/profile/<uuid:id>', views.GetProfileView , name='profile'),
    path('auth/profile/<uuid:id>', views.UpdateProfileView , name='profile'),
    
        # 🔐 JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]