from django.db import models
from users.models import Profile
import uuid
# Create your models here.


class Palindrome(models.Model):
    owner=models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    input= models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.input

    class Meta:
        ordering=['-created']