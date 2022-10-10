from django.urls import path
from . import views 
from .views import RegisterUserAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path ('',views.getRoutes),
    path('palindromes/',views.getPalindromes),
    
    path('palindromes/<str:pk>/',views.getPalindrome),
    path('create-palidrome/',views.createPalindrome),
    path('update-palindrome/<str:pk>/',views.updatePalindrome),
    path('delete-palindrome/<str:pk>/delete/',views.deletePalindrome),

    #user register api
    path('create-user/',RegisterUserAPIView.as_view()), 
]