
from django.urls import path
from . import views


urlpatterns = [
    
   path ('',views.loginUser, name='login'),
   path ('logout/',views.logoutUser,name='logout'),
   path ('register/',views.registerUser,name='register'),
   path ('account/',views.userAccount,name='account'),
   path ('edit-account/',views.editAccount,name='edit-account'),
   path ('delete-account/<str:pk>',views.deleteUser,name='delete-account'),

]
