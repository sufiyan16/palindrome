from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

def createProfile(sender,instance,created,**kwargs):
    if created:
        user=instance       
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )   
       
post_save.connect(createProfile,sender=User)

def deleteUser(sender,instance,**kwargs):
    user=instance.user
    user.delete()
post_delete.connect(deleteUser,sender=Profile)

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
post_save.connect(updateUser, sender=Profile)