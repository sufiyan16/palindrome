
from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.Palindrom,name='palindrome'),
    path('create-pal',views.CreatePal,name='create-pal'),
    path('update-pal/<str:pk>',views.UpdatePal,name='update-pal'),
    path('delete/<str:pk>',views.DeletePal,name='delete'),
]